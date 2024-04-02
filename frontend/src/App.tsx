// import { useState } from "react";
// // import "./App.css";

// export default function App() {
//   const [result, setResult] = useState();
//   const [question, setQuestion] = useState();
//   const [file, setFile] = useState();

//   const handleQuestionChange = (event: any) => {
//     setQuestion(event.target.value);
//   };

//   const handleFileChange = (event: any) => {
//     setFile(event.target.files[0]);
//   };

//   const handleSubmit = (event: any) => {
//     event.preventDefault();

//     const formData = new FormData();

//     if (file) {
//       formData.append("file", file);
//     }
//     if (question) {
//       formData.append("question", question);
//     }

//     fetch("http://127.0.0.1:8000/predict", {
//       method: "POST",
//       body: formData,
//     })
//       .then((response) => response.json())
//       .then((data) => {
//         setResult(data.result);
//       })
//       .catch((error) => {
//         console.error("Error", error);
//       });
//   };

//   return (
//     <div className="appBlock">
//       <form onSubmit={handleSubmit} className="form">
//         <label className="questionLabel" htmlFor="question">
//           Question:
//         </label>
//         <input
//           className="questionInput"
//           id="question"
//           type="text"
//           value={question}
//           onChange={handleQuestionChange}
//           placeholder="Ask your question here"
//         />

//         <br></br>
//         <label className="fileLabel" htmlFor="file">
//           Upload CSV file:
//         </label>

//         <input
//           type="file"
//           id="file"
//           name="file"
//           accept=".csv"
//           onChange={handleFileChange}
//           className="fileInput"
//         />
//         <br></br>
//         <button
//           className="submitBtn"
//           type="submit"
//           disabled={!file || !question}
//         >
//           Submit
//         </button>
//       </form>
//       <p className="resultOutput">Result: {result}</p>
//     </div>
//   );
// }

import React, { useState, ChangeEvent, FormEvent } from "react";
import "./App.css";

export default function App(): JSX.Element {
  const [result, setResult] = useState<string | undefined>();
  const [question, setQuestion] = useState<string | undefined>();
  const [file, setFile] = useState<File | undefined>();

  const handleQuestionChange = (event: ChangeEvent<HTMLInputElement>): void => {
    setQuestion(event.target.value);
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>): void => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>): void => {
    event.preventDefault();

    const formData = new FormData();

    if (file) {
      formData.append("file", file);
    }
    if (question) {
      formData.append("question", question);
    }

    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        setResult(data?.result?.result);
      })
      .catch((error) => {
        console.error("Error", error);
      });
  };

  return (
    <div className="appBlock">
      <form onSubmit={handleSubmit} className="form">
        <label className="questionLabel" htmlFor="question">
          Question:
        </label>
        <input
          className="questionInput"
          id="question"
          type="text"
          value={question || ""}
          onChange={handleQuestionChange}
          placeholder="Ask your question here"
        />

        <br></br>
        <label className="fileLabel" htmlFor="file">
          Upload PDF or Document:
        </label>

        <input
          type="file"
          id="file"
          name="file"
          accept=".pdf,.doc,.docx,.txt" // Accept PDF and other document types
          onChange={handleFileChange}
          className="fileInput"
        />
        <br></br>
        <button
          className="submitBtn"
          type="submit"
          disabled={!file || !question}
        >
          Submit
        </button>
      </form>
      <p className="resultOutput">Result: {result}</p>
    </div>
  );
}
