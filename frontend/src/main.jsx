import "./index.css";
import ReactDOM from "react-dom/client";
import Playground from "$pages/Playground.jsx";
import LandingPage from "$pages/Landing.jsx";
import Layout from "$lib/components/Layout.jsx";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import RegistrationPage from "$pages/RegisterPage.jsx";
import LoginPage from "$pages/LoginPage";
import StudentHomePage from "$pages/StudentHomePage";
import TermsPage from "$pages/TermsPage";
import JoinClassPage from "$pages/JoinClassPage";
import CourseCatalogPage from "$pages/CourseCatalogPage";
import StudentCoursesPage from "$pages/StudentCoursesPage";
import EditProfilePage from "$pages/EditProfilePage";
import TeacherHomePage from "$pages/TeacherHomePage";
import TeacherClassesPage from "$pages/TeacherClassesPage";
import TeacherAssignmentsPage from "$pages/TeacherAssignmentsPage";

const root = document.getElementById("root");

if (!root) {
  throw Error("root element not found");
}


ReactDOM.createRoot(root).render(
  <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/">
            <Route index element={<LandingPage />} />
            <Route path="register" element={<RegistrationPage />} />
            <Route path="login" element={<LoginPage />} />
            <Route path="terms" element={<TermsPage />} />
            <Route path="catalog" element={<CourseCatalogPage />} />
            <Route path="playground" element={<Playground />} />
            <Route path="s/">
              <Route path="home" element={<StudentHomePage />} />
              <Route path="join" element={<JoinClassPage />} />
              <Route path="classes" element={<StudentHomePage />} />
              <Route path="courses" element={<StudentCoursesPage />} />
            </Route>
            <Route path="t/">
              <Route path="home" element={<TeacherHomePage />} />
              <Route path="classes" element={<TeacherClassesPage />} />
              <Route path="c/">
                <Route path=":classid" element={<TeacherAssignmentsPage />} />
              </Route>
            </Route>
            <Route path="u/">
              <Route path="edit" element={<EditProfilePage />} />
            </Route>
          </Route>
        </Routes>
      </Layout>
  </BrowserRouter>,
);
