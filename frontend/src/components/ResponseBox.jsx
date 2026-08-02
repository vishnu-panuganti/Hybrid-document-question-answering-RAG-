function ResponseBox({ response }) {

    return (

        <div className="bg-white rounded-3xl shadow-xl p-8">

            <h2 className="text-3xl font-bold mb-6">
                AI Response
            </h2>

            <div className="bg-gray-100 rounded-2xl p-6 min-h-[150px]">

                <p>

                    {response || "Your answer will appear here..."}

                </p>

            </div>

        </div>

    );

}

export default ResponseBox;