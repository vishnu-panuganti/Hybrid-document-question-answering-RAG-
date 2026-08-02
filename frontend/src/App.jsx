import { useState } from "react";

import Sidebar from "./components/Sidebar";
import PromptBox from "./components/PromptBox";
import Conversation from "./components/Conversation";

function App() {

    const [chats, setChats] = useState([]);

    const [activeChat, setActiveChat] = useState(null);


    return (

        <div className="app-container">

            <Sidebar
                chats={chats}
                setChats={setChats}
                activeChat={activeChat}
                setActiveChat={setActiveChat}
            />

            <div className="main-content">

                <PromptBox

    chats={chats}
    setChats={setChats}

    activeChat={activeChat}
    setActiveChat={setActiveChat}

/>

                <Conversation
    activeChat={activeChat}
/>

            </div>

        </div>

    );

}

export default App;