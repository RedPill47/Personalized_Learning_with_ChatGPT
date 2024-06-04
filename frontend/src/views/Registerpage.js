import React, { useState, useContext } from 'react';
import AuthContext from '../context/AuthContext';
import { Link, useHistory } from 'react-router-dom';
import './style/Auth.css';
import swal from 'sweetalert2';

function RegisterPage() {
  const [step, setStep] = useState(1);
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [learningclass, setLearningclass] = useState("");
  const [learninglevel, setLearninglevel] = useState("");
  const [learningtype, setLearningtype] = useState([]);

  const { registerUser } = useContext(AuthContext);
  const history = useHistory();

  const handleNextStep = () => {
    setStep(step + 1);
  };

  const handlePreviousStep = () => {
    setStep(step - 1);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    registerUser(email, username, learningclass, learninglevel, learningtype, password, password2);
    history.push('/register');
    // Password match validation
    if (password !== password2) {
      swal.fire({
          title: "Passwords do not match",
          icon: "error",
          toast: true,
          timer: 4000,
          position: 'top-right',
          timerProgressBar: true,
          showConfirmButton: true,
          showCancelButton: false,
      });
      return;
    }
  };

  const handleCheckboxChange = (e) => {
    const { value, checked } = e.target;
    setLearningtype((prev) => {
      const types = checked ? [...prev, value] : prev.filter(type => type !== value);
      return types;
    });
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        {step === 1 && (
          <Step1
            email={email}
            setEmail={setEmail}
            username={username}
            setUsername={setUsername}
            password={password}
            setPassword={setPassword}
            password2={password2}
            setPassword2={setPassword2}
            handleNextStep={handleNextStep}
          />
        )}
        {step === 2 && (
          <Step2
            learningclass={learningclass}
            setLearningclass={setLearningclass}
            learninglevel={learninglevel}
            setLearninglevel={setLearninglevel}
            learningtype={learningtype}
            handleCheckboxChange={handleCheckboxChange}
            handlePreviousStep={handlePreviousStep}
            handleSubmit={handleSubmit}
          />
        )}
      </div>
    </div>
  );
}

function Step1({ email, setEmail, username, setUsername, password, setPassword, password2, setPassword2, handleNextStep }) {
  return (
    <>
      <form onSubmit={(e) => { e.preventDefault(); handleNextStep(); }}>
        <h1>Create your account</h1>
        <p>to continue to Tutor AI</p>
        <div className="input-group">
          <label htmlFor="email">Email address</label>
          <input type="email" id="email" name="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div className="input-group">
          <label htmlFor="username">Username</label>
          <input type="text" id="username" name="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
        </div>
        <div className="input-group">
          <label htmlFor="password">Password</label>
          <input type="password" id="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <div className="input-group">
          <label htmlFor="confirm-password">Confirm Password</label>
          <input type="password" id="confirm-password" name="confirm-password" value={password2} onChange={(e) => setPassword2(e.target.value)} required />
        </div>
        <button type="submit" className="auth-button">Continue</button>
      </form>
      <div className="auth-footer">
        <p>Already have an account? <Link to="/login">Sign in</Link></p>
      </div>
    </>
  );
}

function Step2({ learningclass, setLearningclass, learninglevel, setLearninglevel, learningtype, handleCheckboxChange, handlePreviousStep, handleSubmit }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'class') {
      setLearningclass(value);
    } else if (name === 'level') {
      setLearninglevel(value);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>Learning Preferences</h1>
      <div className="input-group">
        <label htmlFor="class">Class</label>
        <select id="class" name="class" value={learningclass} onChange={handleChange}>
          <option value="">Select Class</option>
          <option value="highschool">High School</option>
          <option value="university">University</option>
        </select>
      </div>
      <div className="input-group">
        <label htmlFor="level">Level</label>
        <select id="level" name="level" value={learninglevel} onChange={handleChange}>
          <option value="">Select Level</option>
          <option value="beginner">Beginner</option>
          <option value="intermediary">Intermediary</option>
          <option value="expert">Expert</option>
        </select>
      </div>
      <div className="input-group">
        <label>Type of Lessons and Exercises</label>
        <div className="checkbox-group">
          <input type="checkbox" id="example" value="example" checked={learningtype.includes('example')} onChange={handleCheckboxChange} />
          <label htmlFor="example">With Example</label>
        </div>
        <div className="checkbox-group">
          <input type="checkbox" id="detailed" value="detailed" checked={learningtype.includes('detailed')} onChange={handleCheckboxChange} />
          <label htmlFor="detailed">Detailed Explanations</label>
        </div>
        <div className="checkbox-group">
          <input type="checkbox" id="recommendations" value="recommendations" checked={learningtype.includes('recommendations')} onChange={handleCheckboxChange} />
          <label htmlFor="recommendations">Recommendations</label>
        </div>
      </div>
      <div className="auth-footer">
        <button type="button" onClick={handlePreviousStep} className="auth-button">Back</button>
        <button type="submit" className="auth-button">Register</button>
      </div>
    </form>
  );
}

export default RegisterPage;
