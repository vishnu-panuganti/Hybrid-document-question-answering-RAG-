function Conversation({ activeChat }) {

    // No chat selected.
    if (!activeChat) {
        return (
            <div>
                <p>Start typing to begin a conversation.</p>
            </div>
        );
    }

    return (

        <div>

            {

                activeChat.conversations.map(

                    (conversation, index) => (

                        <div key={index}>

                            {/* User / AI message */}
                            <p>
                                {conversation.message}
                            </p>

                            {/* Attached PDFs */}
                            {

                                conversation.documents.map(

                                    (document, docIndex) => (

                                        <p key={docIndex}>
                                            {document.name}
                                        </p>

                                    )

                                )

                            }

                            <hr />

                        </div>

                    )

                )

            }

        </div>

    );

}

export default Conversation;