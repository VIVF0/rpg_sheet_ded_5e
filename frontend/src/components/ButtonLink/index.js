import React from 'react';
import { Link } from 'react-router-dom';
import './CreateCharacterButton.css'

function ButtonLink(props) {
  return (
    <Link to={props.link}>
      <button className="white-button">
        {props.text}
      </button>
    </Link>
  );
}

export default ButtonLink;
