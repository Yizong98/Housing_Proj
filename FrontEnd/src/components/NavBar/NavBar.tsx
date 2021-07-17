import React, { FunctionComponent } from 'react';
import { Button, ImageDropdown, Link } from '@basics';
import Navbar from 'react-bootstrap/Navbar';
import { useDispatch } from 'react-redux';
import { showLogin } from '@redux';
import { landingIcons } from '@icons';
import styles from './NavBar.module.scss';
import { Row } from 'react-bootstrap';
import { useUser } from '@hooks';

const NavBar: FunctionComponent = () => {
  const dispatch = useDispatch();
  const { data: user, logout } = useUser();
  const itemProps = [
    {
      href: '/profile',
      label: 'Profile',
    },
    {
      label: 'Logout',
      labelClassName: styles.logoutText,
      onClick: logout,
    },
  ];

  return (
    <Navbar sticky="top" className={`${styles.wrapper} p-0 m-0 mb-4`}>
      <div className={styles.container}>
        <div className="mr-auto">
          <a href="/housing">
            <landingIcons.logo className={styles.logo} />
          </a>
        </div>
        <Row className="align-items-center">
          <Link href="/" undecorated>
            <h5 className="mb-0">About</h5>
          </Link>
          {user.isLoggedIn ? (
            <ImageDropdown
              items={itemProps}
              profileIcon={user.profilePhoto}
              className="ml-4"
            />
          ) : (
            <Button
              size="secondary"
              variant="solid"
              onClick={() => dispatch(showLogin())}
            >
              Get Started
            </Button>
          )}
        </Row>
      </div>
    </Navbar>
  );
};

export default NavBar;
