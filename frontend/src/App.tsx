import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "@/components/Navbar";
import HomePage from "@/pages/HomePage";
import SearchPage from "@/pages/SearchPage";
import QnAPage from "@/pages/QnAPage";
import AddDocumentPage from "@/pages/AddDocumentPage";

export default function App() {
  return (
    <Router>
      <Navbar/>
      <div style={{ padding: "2rem" }}>
        <Routes>
          <Route path="/" element={<HomePage/>}/>
          <Route path="/search" element={<SearchPage/>}/>
          <Route path="/qna" element={<QnAPage/>}/>
          <Route path='/add-document' element={<AddDocumentPage/>}/>
        </Routes>
      </div>
    </Router>
  );
}
