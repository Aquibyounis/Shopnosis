const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");
const multer = require("multer");
const path = require("path");
const fs = require("fs");

const app = express();
const port = 4000;

// Middleware
app.use(express.json());
app.use(cors());

// Connect to MongoDB
mongoose.connect("mongodb://127.0.0.1:27017/Shopnosis", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log("Connected to MongoDB"))
.catch((err) => console.error("MongoDB connection error:", err));


// User Schema and Model
const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, unique: true, required: true },
  password: { type: String, required: true },
  date: { type: Date, default: Date.now }
});

const User = mongoose.model("User", userSchema);

// File Schema and Model
const fileSchema = new mongoose.Schema({
  filename: String,
  originalname: String,
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
  uploadDate: { type: Date, default: Date.now }
});
const File = mongoose.model("File", fileSchema);

// Multer setup for file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, "uploads"));
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + "-" + file.originalname);
  }
});
const upload = multer({ storage });

// Root endpoint
app.get("/", (req, res) => {
  res.send("Welcome to Shopnosis API");
});

// Signup endpoint
app.post("/signup", async (req, res) => {
  try {
    const { name, email, password } = req.body;

    if (!name || !email || !password) {
      return res.status(400).json({ success: false, error: "Name, email, and password are required" });
    }

    // Check if user already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ success: false, error: "User with this email already exists" });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Create user
    const newUser = new User({ name, email, password: hashedPassword });
    await newUser.save();

    // Create JWT token
    const token = jwt.sign({ userId: newUser._id }, "secret_shopnosis", { expiresIn: "15d" });

    // Return name in response
    res.json({ success: true, token, name: newUser.name });
  } catch (error) {
    console.error("Signup error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// Login endpoint
app.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ success: false, error: "Email and password are required" });
    }

    // Find user by email
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(400).json({ success: false, error: "Invalid email or password" });
    }

    // Compare password
    const validPassword = await bcrypt.compare(password, user.password);
    if (!validPassword) {
      return res.status(400).json({ success: false, error: "Invalid email or password" });
    }

    // Create JWT token
    const token = jwt.sign({ userId: user._id }, "secret_shopnosis", { expiresIn: "15d" });

    // Return name in response
    res.json({ success: true, token, name: user.name });
  } catch (error) {
    console.error("Login error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// Basic auth middleware to protect routes
const authenticate = (req, res, next) => {
  const token = req.header("auth-token");
  if (!token) return res.status(401).json({ error: "Access denied. No token provided." });

  try {
    const verified = jwt.verify(token, "secret_shopnosis");
    req.user = verified;
    next();
  } catch (err) {
    res.status(401).json({ error: "Invalid token" });
  }
};

// Example protected route (optional)
app.get("/protected", authenticate, (req, res) => {
  res.json({ message: "You accessed a protected route!", userId: req.user.userId });
});

// Get all users (protected route)
app.get("/users", authenticate, async (req, res) => {
  try {
    const users = await User.find({}, "-password"); // Exclude password field
    res.json({ success: true, users });
  } catch (error) {
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// Upload file endpoint (protected)
app.post("/filesupload", authenticate, upload.single("file"), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ success: false, error: "No file uploaded" });
    const newFile = new File({
      filename: req.file.filename,
      originalname: req.file.originalname,
      userId: req.user.userId
    });
    await newFile.save();
    res.json({ success: true, file: newFile });
  } catch (error) {
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// Get files for logged-in user (protected)
app.get("/myfiles", authenticate, async (req, res) => {
  try {
    const files = await File.find({ userId: req.user.userId });
    res.json({ success: true, files });
  } catch (error) {
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// Change password (forgot password)
app.post("/changepassword", async (req, res) => {
  try {
    const { email, newPassword } = req.body;
    if (!email || !newPassword) {
      return res.status(400).json({ success: false, error: "Email and new password are required" });
    }
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(404).json({ success: false, error: "User not found" });
    }
    user.password = await bcrypt.hash(newPassword, 10);
    await user.save();
    res.json({ success: true, message: "Password changed successfully" });
  } catch (error) {
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// Delete file endpoint (protected)
app.delete("/deletefile/:id", authenticate, async (req, res) => {
  try {
    const file = await File.findOneAndDelete({ _id: req.params.id, userId: req.user.userId });
    if (!file) return res.status(404).json({ success: false, error: "File not found" });
    // Delete file from disk
    const filePath = path.join(__dirname, "uploads", file.filename);
    if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Shopnosis backend running on port ${port}`);
});
