require("dotenv").config();
const cors= require("cors");
const express = require("express");
const connectDB = require("./connectDB");
const Book = require("./models/Books");
const multer = require("multer");
const fs = require("fs");
let {PythonShell} = require('python-shell')

const app = express();
const PORT = process.env.PORT || 8000;
const path = require('path');

// Construct the absolute path to the Python script using __dirname
const scriptPath = path.join(__dirname, 'test.py');
connectDB();
app.use(cors());
app.use(express.urlencoded({ extended: true } ));
app.use(express.json());
app.use("/uploads", express.static("uploads"));


app.get("/api/books", async (req, res) => {
  try {
    const category = req.query.category;
    const filter = {}
    if(category) {
      filter.category = category;
    }
    const data = await Book.find(filter);
    res.json(data);
  } catch (error) {
    res.status(500).json({error: "An error occured while fetching books"});
  }
})


app.post("/python", async (req, res) => {
  const code = req.body.value;
  const input = req.body.input;
  const outpu = req.body.output;
  const testCaseResults = [];

  fs.writeFileSync("test.py", code);


  const inputArray =input.split(' ').map(Number);

    console.log(inputArray);
      let output = parseInt(outpu);
      inputArray.push(output); 
      console.log(inputArray);
  const options = {
    mode: "text",
    pythonOptions: ["-u"],
    args: inputArray,
};

const pythonResults = await PythonShell.run("test.py", options);
testCaseResults.push(pythonResults);
console.log(testCaseResults );
res.json({ testCaseResults });
});
 
app.get("/api/books/:slug", async (req, res) => {
  try {
    const slugParam = req.params.slug;
    const data = await Book.findOne({ slug: slugParam});
    if(!data) {
      throw new Error("Error while fetching data for a book");
    }

    res.status(201).json(data);

  } catch (error) {
    res.status(500).json({error: "An error occured while fetching books"});
  }
});



// add book now

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/')
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9)
    cb(null, uniqueSuffix + "-" + file.originalname);
  }
})

const upload = multer({ storage: storage })

app.post("/api/books", upload.single("thumbnail")  ,async (req, res) => {
  try {
    console.log(req.body);
    console.log(req.file);

    const newBook = new Book({
      title: req.body.title,
      slug: req.body.slug,
      stars: req.body.stars,
      description: req.body.description,
      category: req.body.category,
      thumbnail: req.file.filename,
      username: req.body.username,
      solution:req.body.solution,
      input:req.body.input,
      output:req.body.output,
    })

    await Book.create(newBook);
    res.json("Data Submitted");
  } catch (error) {
    res.status(500).json({ error: "An error occurred while fetching books." });
  }
});


app.put("/api/books", upload.single("thumbnail"), async (req, res) => {
  try {

    const bookId = req.body.bookId;

    const updateBook = {
      title: req.body.title,
      slug: req.body.slug,
      stars: req.body.stars,
      description: req.body.description,
      category: req.body.category,
      username: req.body.username,
    }

    if (req.file) {
      updateBook.thumbnail = req.file.filename;
    }

    await Book.findByIdAndUpdate(bookId, updateBook)
    res.json("Data Submitted");
  } catch (error) {
    res.status(500).json({ error: "An error occurred while fetching books." });
  }
});


app.delete("/api/books/:id", async(req,res) => {
  const bookId = req.params.id;

  try {
    await Book.deleteOne({_id: bookId});
    res.json("How dare you!" + req.body.bookId);
  } catch (error) {
    res.json(error);
  }
});





// TRIAL


app.get("/", (req, res) => {
    res.json("This is the home page.");
});

app.get("*", (req, res) => {
    res.sendStatus("404");
});

app.listen(PORT, () => {
    console.log(`Sever running at Port: ${PORT}`)
});