import { useState } from "react";
import axios from "axios";

function UploadPDF() {

    const [file, setFile] = useState(null);

    const uploadPDF = async () => {

        if (!file) {
            alert("Please select a PDF.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {

            const res = await axios.post(
                "http://127.0.0.1:8000/upload",
                formData
            );

            alert(res.data.message);

        } catch (error) {
            console.log(error);
            alert("Upload failed!");
        }

    };


    return (

        <div className="bg-white rounded-3xl shadow-xl p-8">

            <h2 className="text-3xl font-bold mb-6">
                Upload PDF
            </h2>

            <div className="border-2 border-dashed border-gray-300 rounded-2xl p-10 text-center">

                <input
                    type="file"
                    onChange={(e) => setFile(e.target.files[0])}
                />

            </div>

            <button
                onClick={uploadPDF}
                className="mt-6 bg-black text-white px-6 py-3 rounded-xl"
            >
                Upload PDF
            </button>

        </div>

    );
}

export default UploadPDF;