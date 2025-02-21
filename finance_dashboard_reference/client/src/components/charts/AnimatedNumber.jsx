import React, { useEffect, useState } from "react";

const AnimatedNumber = ({ value, duration = 1000 }) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let start = 0;
    const increment = Math.ceil(value / (duration / 10));
    
    const timer = setInterval(() => {
      start += increment;
      if (start >= value) {
        setCount(value);
        clearInterval(timer);
      } else {
        setCount(start);
      }
    }, 10);

    return () => clearInterval(timer);
  }, [value, duration]);

  return <h2 style={{ fontSize: "2em", color: "#4A90E2", transition: "0.5s ease-in-out" }}>{count.toLocaleString()}</h2>;
};

export default AnimatedNumber;
