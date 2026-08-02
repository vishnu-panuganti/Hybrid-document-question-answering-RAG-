import { useState } from "react";
import axios from "axios";

function QuestionBox({ setResponse }) {

    const [question, setQuestion] = useState("");

    const askQuestion = async () => {

        try {

            const res = await axios.post(
                "http://127.0.0.1:8000/ask",
                {
                    question: question
                }
            );

            setResponse(res.data.answer);

        } catch (error) {

            console.log(error);
            alert("Something went wrong!");

        }

    };


    return (

        <div className="bg-white rounded-3xl shadow-xl p-8">

            <h2 className="text-3xl font-bold mb-6">
                Ask a Question
            </h2>

            <input
                type="text"
                placeholder="Ask anything about your PDF..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="w-full p-4 rounded-xl border"
            />

            <button
                onClick={askQuestion}
                className="mt-6 bg-blue-600 text-white px-6 py-3 rounded-xl"
            >
                Ask Question
            </button>

        </div>

    );
}

export default QuestionBox;