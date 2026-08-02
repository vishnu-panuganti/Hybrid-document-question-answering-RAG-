import { useState } from "react";

function Sidebar({

    chats,
    setChats,

    activeChat,
    setActiveChat

}) {

    const [isOpen, setIsOpen] = useState(false);


    const toggleSidebar = () => {
        setIsOpen((prev) => !prev);
    };


    const createNewChat = () => {

        const newChat = {

            id: Date.now(),

            title: `Chat ${chats.length + 1}`,

            conversations: [],

           

            createdAt: Date.now()

        };

        setChats([newChat, ...chats]);

        setActiveChat(newChat);

    };


    return (

        <div className="sidebar">

            <button onClick={toggleSidebar}>
                ☰
            </button>


            {isOpen && (

                <div>

                    <h1>AskPDF AI</h1>

                    <button onClick={createNewChat}>
                        + New Chat
                    </button>

                    <hr />

                    <h2>Chats</h2>


                    {

                        chats.length === 0 ?

                            <p>No Chats Yet</p>

                            :

                            chats.map((chat) => (

                                <p
                                    key={chat.id}
                                    onClick={() => setActiveChat(chat)}
                                >

                                    {chat.title}

                                    {activeChat?.id === chat.id &&
                                        " (Active)"}

                                </p>

                            ))

                    }

                </div>

            )}

        </div>

    );

}

export default Sidebar;