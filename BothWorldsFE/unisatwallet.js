document.addEventListener('DOMContentLoaded', function() {
    const walletButton = document.getElementById('walletButton');
    let isUniSatWalletConnected = false;
    let walletAddress = '';

    // Function to connect to UniSat Wallet
    async function connectUniSatWallet() {
        console.log("Attempting to connect UniSat Wallet");
        try {
            if (window.unisat) {
                await window.unisat.requestAccounts();
                const addresses = await window.unisat.getAccounts();

                if (addresses && addresses.length > 0) {
                    walletAddress = addresses[0]; // Save the first address
                    isUniSatWalletConnected = true;
                    updateWalletButton();
                } else {
                    console.log("No UniSat Wallet addresses found.");
                    isUniSatWalletConnected = false;
                }
            } else {
                console.log("UniSat Wallet is not installed.");
                isUniSatWalletConnected = false;
            }
        } catch (err) {
            console.error("Error connecting to UniSat Wallet: ", err);
            isUniSatWalletConnected = false;
        }
    }

    // Function to disconnect UniSat Wallet
    function disconnectUniSatWallet() {
        walletAddress = '';
        isUniSatWalletConnected = false;
        updateWalletButton();
    }

    // Function to update the Wallet button text
    function updateWalletButton() {
        if (isUniSatWalletConnected) {
            walletButton.innerText = walletAddress;
        } else {
            walletButton.innerText = 'Wallet';
        }
    }

    // Initial setup
    walletButton.addEventListener('click', function() {
        if (isUniSatWalletConnected) {
            disconnectUniSatWallet();
        } else {
            connectUniSatWallet();
        }
    });

    updateWalletButton();
});