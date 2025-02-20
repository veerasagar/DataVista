import express from "express";
import fileUpload from "express-fileupload";

const router = express.Router();
router.use(fileUpload()); // ✅ Enables file uploads

router.post("/upload", async (req, res) => {
    if (!req.files || !req.files.file) {
        return res.status(400).json({ error: "No file uploaded!" });
    }

    const uploadedFile = req.files.file;
    console.log("File received:", uploadedFile.name);

    res.json({ message: "File uploaded successfully!", file: uploadedFile.name });
});

export default router;
