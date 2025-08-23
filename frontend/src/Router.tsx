import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import ForehandPractice from "./pages/ForehandPractice";
import BackhandPractice from "./pages/BackhandPractice";
import AlternationChallenge from "./pages/AlternationChallenge";
import RallyLongevity from "./pages/RallyLongevity";

const Router = () => {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/practice/forehand" element={<ForehandPractice />} />
      <Route path="/practice/backhand" element={<BackhandPractice />} />
      <Route path="/practice/alternation" element={<AlternationChallenge />} />
      <Route path="/practice/rally" element={<RallyLongevity />} />
    </Routes>
  );
};

export default Router;
