import React, { useState, useEffect } from "react";
const DataFetcher = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/posts"); // Endpoint URL
        console.log("***RESPONSE_IS****", response);
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const responseData = await response.json();
        console.log("RESPONSE_DATA_IS", responseData);
        setData(responseData);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  let TitleName = data.title;
  console.log("Title_is", TitleName);
  return (
    <div>
      {/* Display your fetched data here */}
      {data && (
        <ol>
          {data.map((data) => (
            <>
              <li>
                <div>
                  {" "}
                  <b>Title:</b> {data.title}
                </div>
                <br></br>
                <div>
                  {" "}
                  <b>Content:</b> {data.content}
                </div>
                <br></br>
                <div>
                  {" "}
                  <b>User Information: </b>
                  <ul>
                    <div>
                      <b>UserName: </b>
                      {data.user.name}
                    </div>
                    <div>
                      <b>Email: </b>
                      {data.user.email}
                    </div>
                  </ul>
                </div>
                <br></br>
              </li>
            </>
          ))}
        </ol>
      )}
    </div>
  );
};

export default DataFetcher;
