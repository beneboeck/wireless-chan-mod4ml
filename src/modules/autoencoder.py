import torch
import torch.nn as nn
import numpy as np
from utils import torch_utils as tu

class autoencoder(nn.Module):
    def __init__(self, device, dim, ch_factor=2, n_conv=3, ld=32):
        """
        class for the autoencoder implementation including the training routine

        Parameters:
        -------------
        device: str
            stores the device on which the autoencoder is stored (either 'cpu' or 'cuda:some_number')
        dim: list of two entries
            encodes the number of subcarriers and time symbols
        ch_factor: int
            encodes a multiplication factor for the number of convolutional channels in the en- and decoder
        n_conv: int
            number of convolutional layers in the autoencoder
        ld: int
            latent dimension
        """
        super().__init__()
        self.device = device
        self.ch_factor = ch_factor
        self.n_conv = n_conv
        self.latent_dim = ld
        self.dim = dim

        # build the Encoder
        in_dim = 2
        next_dim = in_dim * 4 * self.ch_factor
        dim1_out, dim2_out, ch_out = tu.calculate_dim_after_convBlock(self.dim[0], self.dim[1], self.n_conv, 2)
        conv_out_dim = dim1_out * dim2_out * ch_out
        encoder = []
        for i in range(self.n_conv):
            encoder.append(nn.Conv2d(in_dim,next_dim,3,2,1))
            encoder.append(nn.ReLU())
            in_dim = next_dim
            next_dim = in_dim * 4
        encoder.append(nn.Flatten())
        encoder.append(nn.Linear(conv_out_dim*self.ch_factor,self.latent_dim))
        encoder.append(nn.Tanh())
        self.encoder = nn.Sequential(*encoder)

        # build the Decoder
        decoder = []
        decoder.append(nn.Linear(self.latent_dim,conv_out_dim*self.ch_factor))
        decoder.append(nn.Unflatten(1,(4**self.n_conv * 2 *self.ch_factor,6,2)))
        decoder.append(nn.ConvTranspose2d(4**self.n_conv * 2*self.ch_factor,32*self.ch_factor,4,2,1))
        decoder.append(nn.ReLU())
        decoder.append(nn.ConvTranspose2d(32 * self.ch_factor, 8 * self.ch_factor, (4, 3), 2, 1))
        decoder.append(nn.ReLU())
        decoder.append(nn.ConvTranspose2d(8*self.ch_factor,8*self.ch_factor,4,2,1))
        decoder.append(nn.ReLU())
        decoder.append(nn.Conv2d(8*self.ch_factor,2,1))
        self.decoder = nn.Sequential(*decoder)

    def forward(self, x):
        """
        simple forward routine

        Parameters:
        -----------
        x: torch.tensor of shape [batch_size, 2, n_subcarrier, n_symbols]
            stores a batch of real-valued channel realizations

        Returns:
        -----------
        x_hat: torch.tensor of shape [batch_size, 2, n_subcarrier, n_symbols]
            stores the reconstructed real-valued channel realizations
        """
        z = self.encoder(x)
        x_hat = self.decoder(z)
        return x_hat

    def fit(self, lr, miter, dl_train, dl_val):
        """
        the training routine for the autoencoder

        Parameters:
        -------------
        lr: float
            stores the learning rate
        miter: int
            stores the number of maximal training iterations
        dl_train: DataLoader
            stores the DataLoader for training (should be loader that outputs batched torch.tensors (no list of tensors))
        dl_val: DataLoader
            stores the DataLoader for validation (should be loader that outputs batched torch.tensors (no list of tensors))

        Returns:
        -----------
        risk_val: list of numpy numbers
            saves the risk over the validation set during training
        """

        # define optimizer and scheduler
        optimizer = torch.optim.Adam(lr=lr, params=self.parameters())
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer = optimizer, step_size = 30, gamma = 0.9)

        # initialize some tracking lists
        risk_val = np.zeros(miter)

        # iterate through the epochs
        for i in range(miter):
            for ind, samples in enumerate(dl_train):
                sample_in = samples.to(self.device)
                sample_hat = self.forward(sample_in)
                # compute normalized MSE as objective (normalization doesn't play a big role here)
                risk = torch.mean(torch.sum(torch.abs(sample_hat - sample_in)**2,dim=(1,2,3)))/(self.dim[0] * self.dim[1])
                # backpropagation
                optimizer.zero_grad()
                risk.backward()
                optimizer.step()
            # scheduler update
            scheduler.step()

            # track the validation loss
            with torch.no_grad():
                # you can customize how often you want to track the validation loss
                if i % 1 == 0:
                    risk_total = []
                    i5 = i
                    #i5 = int(i / 3)
                    self.eval()
                    for ind, samples in enumerate(dl_val):
                        sample_in = samples.to(self.device)
                        sample_hat = self.forward(sample_in)
                        risk = torch.mean(torch.sum(torch.abs(sample_hat - sample_in) ** 2, dim=(1, 2, 3)))/(self.dim[0] * self.dim[1])
                        risk_total.append(risk.detach().to('cpu').numpy())
                    # simply print out some updates from time to time
                    if i % 3 == 0:
                        print(f'validation risk after {i} iterations: {np.mean(np.array(risk_total)):.4f}')
                    risk_val[i5] = np.mean(np.array(risk_total))
                    # check for early stopping (customized)
                    if i > 100:
                        steps = 20
                        x_range_lr = torch.arange(steps)
                        x_lr = torch.ones(steps, 2)
                        x_lr[:, 0] = x_range_lr
                        beta_lr = torch.linalg.inv(x_lr.T @ x_lr) @ x_lr.T @ risk_val[i5-steps+1:i5+1][:, None]
                        slope_lr = beta_lr[0].detach().to('cpu').numpy()[0]
                        if i % 3 == 0:
                            print(f'slope risk val: {slope_lr}')
                        if slope_lr > 0:
                            break
                    self.train()
        return risk_val[:i5+1]