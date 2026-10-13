import { useState, useRef } from "react";
import axios from "axios";

function PromptBox({

    chats,
    setChats,

    activeChat,
    setActiveChat

})  {

    // Stores whatever the user types in the prompt box.
    const [prompt, setPrompt] = useState("");

    // Temporarily stores all selected PDF documents.
    const [attachedDocuments, setAttachedDocuments] = useState([]);
// Tracks whether the AI is generating a response.
const [isLoading, setIsLoading] = useState(false);
    const fileInputRef = useRef(null);
    



    // =====================================
    // Handles PDF selection from file picker.
    // =====================================
   const handleFileUpload = async (event) => {

    const files = Array.from(event.target.files);

    setAttachedDocuments((prev) => [
        ...prev,
        ...files
    ]);

    for (const file of files) {

        const formData = new FormData();

        formData.append("file", file);

        try {
            

            const response = await axios.post(
                "http://127.0.0.1:8000/upload",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }
            );

            console.log(response.data);

        } catch (error) {

            console.error(error);

        }

    }

};


    // =====================================
    // Removes a selected PDF.
    // =====================================
    const removeDocument = (index) => {

        // Keeps every file except the one whose index matches.
        const updatedDocuments = attachedDocuments.filter(
            (_, i) => i !== index
        );

        // Updates the state.
        setAttachedDocuments(updatedDocuments);

    };


    // =====================================
    // Handles Send button click.
    // (Temporary implementation)
    // =====================================
 const sendPrompt = async () => {

    if (
        prompt.trim() === "" &&
        attachedDocuments.length === 0
    ) {
        return;
    }

    const conversationObject = {
        role: "user",
        message: prompt,
        documents: attachedDocuments
    };

    let updatedChat;
    let updatedChats;

    // Create chat if it doesn't exist
    if (!activeChat) {

        updatedChat = {
            id: Date.now(),
            title: prompt || "New Chat",
            conversations: [conversationObject]
        };

        updatedChats = [updatedChat, ...chats];

    } else {

        updatedChat = {
            ...activeChat,
            conversations: [
                ...activeChat.conversations,
                conversationObject
            ]
        };

        updatedChats = chats.map(chat =>
            chat.id === updatedChat.id ? updatedChat : chat
        );
    }

    setChats(updatedChats);
    setActiveChat(updatedChat);

    try {
        setIsLoading(true);

        const response = await axios.post(
            "http://127.0.0.1:8000/ask",
            {
                question: prompt
            }
        );

      const aiConversation = {
        role: "assistant",
        message: response.data.answer,
        documents: [],
        sources: response.data.sources || []
};

        const finalChat = {
            ...updatedChat,
            conversations: [
                ...updatedChat.conversations,
                aiConversation
            ]
        };

        const finalChats = updatedChats.map(chat =>
            chat.id === finalChat.id ? finalChat : chat
        );

        setChats(finalChats);
        setActiveChat(finalChat);

    } catch (error) {

        console.error(error);

    }

    setPrompt("");
    setAttachedDocuments([]);
};

   
    const openFilePicker = () => {
    fileInputRef.current.click();
};


    // =====================================
    // UI starts here.
    // =====================================
    return (

        <div>

            {/* Main Heading */}
            <h2>AskPDF AI</h2>

            {/* Small Description */}
            <p>
                Chat with your documents intelligently.
            </p>

            <br />


            {/* Displays attached PDFs */}
            <h3>Attached Documents</h3>

            {
                attachedDocuments.length === 0 ? (

                    <p>No Documents Attached</p>

                ) : (

                    attachedDocuments.map((file, index) => (

                        <div key={index}>

                            {/* Displays PDF name */}
                            {file.name}

                            {/* Removes selected PDF */}
                            <button
                                onClick={() => removeDocument(index)}
                            >
                                X
                            </button>

                        </div>

                    ))

                )
            }


            <br />


            {/* Hidden file input */}
          <input
    type="file"
    accept=".pdf"
    multiple
    hidden
    ref={fileInputRef}
    onChange={handleFileUpload}
/>

            {/* '+' button (functionality will be added later) */}
           <button onClick={openFilePicker}>
    +
</button>


            {/* Prompt input field */}
            <input
                type="text"
                placeholder="Ask anything about your documents..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onKeyDown={(e) => {

    if (e.key === "Enter") {
        sendPrompt();
    }

}}
            />


            {/* Send button */}
            <button onClick={sendPrompt}>
                Send
            </button>


        </div>

    );

}

export default PromptBox;