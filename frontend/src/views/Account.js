import React, { useState, useEffect, useContext } from 'react';
import './style/Account.css';
import useAxios from '../utils/useAxios';
import AuthContext from '../context/AuthContext';
import swal from 'sweetalert2';

const Account = () => {
  const { user } = useContext(AuthContext);
  const api = useAxios();

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [learningClass, setLearningClass] = useState('');
  const [learningLevel, setLearningLevel] = useState('');
  const [lessonTypes, setLessonTypes] = useState([]);
  const [editMode, setEditMode] = useState(false);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await api.get(`/update/${user.user_id}/`);
        const userData = response.data;
        setUsername(userData.username);
        setEmail(userData.email);
        setLearningClass(userData.learning_class);
        setLearningLevel(userData.learning_level);
        setLessonTypes(userData.lesson_types);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };

    fetchUserData();
  }, []); // Fetch user data only once when the component mounts

  const handleCheckboxChange = (e) => {
    const { value, checked } = e.target;
    setLessonTypes((prev) => {
      const types = checked ? [...prev, value] : prev.filter(type => type !== value);
      return types;
    });
  };

  const toggleEditMode = () => {
    setEditMode(!editMode);
  };

  const handleSave = async () => {
    const updatedData = {
      username,
      email,
      password,
      learning_class: learningClass,
      learning_level: learningLevel,
      lesson_types: lessonTypes
    };

    try {
      const response = await api.put(`/update/${user.user_id}/`, updatedData);
      console.log('Account updated successfully:', response.data);
      swal.fire({
        title: "Account updated successfully!",
        icon: "success",
        toast: true,
        timer: 4000,
        position: 'top-right',
        timerProgressBar: true,
        showConfirmButton: false,
        showCancelButton: false,
    });
      setEditMode(false); // Exit edit mode after saving
    } catch (error) {
      console.error('Error updating account:', error);
      alert('Failed to update account. Please try again.');
    }
  };

  return (
    <div className="account-wrapper">
      <div className="main-content">
        <div className="account-section">
          <div className="account-container">
            <h2>Account Settings</h2>
            <form id="accountForm" onSubmit={(e) => e.preventDefault()}>
              <div className="input-group">
                <label htmlFor="username">Username</label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  readOnly={!editMode}
                  required
                />
              </div>
              <div className="input-group">
                <label htmlFor="email">Email Address</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  readOnly={!editMode}
                  required
                />
              </div>
              <div className="input-group">
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  readOnly={!editMode}
                />
              </div>
              <div className="input-group">
                <label htmlFor="learningClass">Learning Class</label>
                <select
                  id="learningClass"
                  name="learningClass"
                  value={learningClass}
                  onChange={(e) => setLearningClass(e.target.value)}
                  disabled={!editMode}
                  required
                >
                  <option value="">Select Class</option>
                  <option value="highschool">High School</option>
                  <option value="university">University</option>
                </select>
              </div>
              <div className="input-group">
                <label htmlFor="learningLevel">Learning Level</label>
                <select
                  id="learningLevel"
                  name="learningLevel"
                  value={learningLevel}
                  onChange={(e) => setLearningLevel(e.target.value)}
                  disabled={!editMode}
                  required
                >
                  <option value="">Select Level</option>
                  <option value="beginner">Beginner</option>
                  <option value="intermediary">Intermediary</option>
                  <option value="expert">Expert</option>
                </select>
              </div>
              <div className="input-group">
                <label>Type of Lessons and Exercises</label>
                <div className="checkbox-group">
                  <input
                    type="checkbox"
                    id="example"
                    value="example"
                    checked={lessonTypes.includes('example')}
                    onChange={handleCheckboxChange}
                    disabled={!editMode}
                  />
                  <label htmlFor="example">With Example</label>
                </div>
                <div className="checkbox-group">
                  <input
                    type="checkbox"
                    id="detailed"
                    value="detailed"
                    checked={lessonTypes.includes('detailed')}
                    onChange={handleCheckboxChange}
                    disabled={!editMode}
                  />
                  <label htmlFor="detailed">Detailed Explanations</label>
                </div>
                <div className="checkbox-group">
                  <input
                    type="checkbox"
                    id="recommendations"
                    value="recommendations"
                    checked={lessonTypes.includes('recommendations')}
                    onChange={handleCheckboxChange}
                    disabled={!editMode}
                  />
                  <label htmlFor="recommendations">Recommendations</label>
                </div>
              </div>
              {editMode ? (
                <button type="button" className="account-button" onClick={handleSave}>Save</button>
              ) : (
                <button type="button" className="account-button" onClick={toggleEditMode}>Edit</button>
              )}
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Account;
