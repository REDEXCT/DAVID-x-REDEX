const express = require('express');
const axios = require('axios');
const FormData = require('form-data');
const multer = require('multer');
const fs = require('fs');
const upload = multer({ dest: 'uploads/' }).array('files', 81);

const app = express();
const port = 3000;

let uploadCount = 0; // Counter to track the number of uploads

app.post('/upload', upload, async (req, res) => {
  try {
    const responses = [];
    for (const file of req.files) {
      uploadCount++;
      let rarity = determineRarity(uploadCount);

      // Upload file to IPFS
      const fileIpfsHash = await uploadToIPFS(file.path);

      // Create metadata for each file
      const metadata = createMetadata(file, uploadCount, rarity, fileIpfsHash);
      const metadataPath = `uploads/metadata${uploadCount}.json`;
      fs.writeFileSync(metadataPath, JSON.stringify(metadata));

      // Upload metadata file to IPFS
      const metadataIpfsHash = await uploadToIPFS(metadataPath);
      responses.push({ fileIpfsHash, metadataIpfsHash, rarity });

      // Clean up the temporary files
      fs.unlinkSync(file.path);
      fs.unlinkSync(metadataPath);
    }

    res.json(responses);
  } catch (error) {
    console.error("Error uploading to IPFS: ", error);
    res.status(500).send("Error uploading to IPFS");
  }
});


function determineRarity(count) {
  if (count <= 9) return 'Extremely Rare';
  if (count <= 45) return 'Very Rare';
  return 'Common';
}

function createMetadata(file, count, rarity, fileIpfsHash) {
  return {
    name: `BothWorlds #${count}`,
    description: 'BothWorlds awaits',
    rarity: rarity,
    fileIpfsHash: fileIpfsHash, // IPFS hash of the file
    uploadMonth: 'December 2023' // Static value for upload month
    // Add other metadata properties if needed
  };
}

async function uploadToIPFS(filePath) {
  const formData = new FormData();
  formData.append("file", fs.createReadStream(filePath));

  const response = await axios.post('https://ipfs.infura.io:5001/api/v0/add', formData, {
    headers: {
      "Authorization": "Basic " + Buffer.from('2X27zN1ZNXDdjMP08hIvwPCB3oC:43c9377e34224412147f69e4844d98b7').toString('base64'),
      ...formData.getHeaders()
    }
  });

  return response.data.Hash;
}

app.post('/upload', upload, async (req, res) => {
    try {
      const responses = [];
      for (const file of req.files) {
        // Use the uploadToIPFS function to upload each file
        const ipfsHash = await uploadToIPFS(file.path);
  
        // Add the hash to the response array
        responses.push(ipfsHash);
  
        // Delete the file from the temporary storage after upload
        fs.unlinkSync(file.path);
      }
  
      res.json(responses);
    } catch (error) {
      console.error("Error uploading to IPFS: ", error);
      res.status(500).send("Error uploading to IPFS");
    }
  });
  
  app.listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
