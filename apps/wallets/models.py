from django.db import models

class CryptoWallet(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the wallet (e.g., Bitcoin, Ethereum).")
    network = models.CharField(max_length=255, help_text="The blockchain network (e.g., Mainnet, Testnet).")
    address = models.CharField(max_length=255, unique=True, help_text="The unique wallet address.")

    def __str__(self):
        return f"{self.name} - {self.network} ({self.address})"
