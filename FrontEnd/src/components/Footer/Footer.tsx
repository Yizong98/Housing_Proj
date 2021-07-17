import React, { FunctionComponent } from 'react';
import cn from 'classnames';
import styles from './Footer.module.scss';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { Link, Subtitle1, Subtitle2, Button } from '@basics';
import { miscIcons } from '@icons';
import { showLogin } from '@redux';
import { useDispatch } from 'react-redux';

const FirstColumn: FunctionComponent = () => {
  const dispatch = useDispatch();

  return (
    <div className={cn(styles.marginBottomProvider, 'px-md-0 px-3')}>
      <Button
        variant="wrapper"
        className={styles.getStarted}
        onClick={() => dispatch(showLogin())}
      >
        <h5>Get Started</h5>
      </Button>

      <Link href="/" undecorated>
        <Subtitle1>About</Subtitle1>
      </Link>

      <Link href="/" undecorated>
        <Subtitle1>Join Us</Subtitle1>
      </Link>
    </div>
  );
};

const homehubEmail = 'homehubdope@gmail.com';

const Email = () => (
  <Link href={`mailto:${homehubEmail}`} external undecorated>
    <Subtitle1 className={cn(styles.greyedOut, styles.email)}>
      {homehubEmail}
    </Subtitle1>
  </Link>
);

const SecondColumn: FunctionComponent = () => (
  <div className={styles.marginBottomProvider}>
    <div>
      <h5>Got feedback or questions?</h5>
    </div>

    <Subtitle1>
      Shoot us an email @ <Email />
    </Subtitle1>

    <Subtitle1 className={styles.greyedOut}>
      {/* copyright symbol */}
      &copy; All rights reserved @Homehub 2020
    </Subtitle1>
  </div>
);

const ThirdColumn: FunctionComponent = () => (
  <div className={cn(styles.marginBottomProvider, styles.homehubOrange)}>
    <Row>
      <Col className={styles.homehubLabel}>
        <Link href="/housing" undecorated>
          <h4 className={styles.homehubOrange}>Homehub</h4>
        </Link>
      </Col>

      <Col className="text-lg-right text-xl-right">
        <Link href="/housing" undecorated>
          <miscIcons.Logo />
        </Link>
      </Col>
    </Row>

    <Subtitle2 className={styles.ellipses}>
      By students <miscIcons.ellipse /> For students <miscIcons.ellipse /> With
      students
    </Subtitle2>
  </div>
);

/**
 * The footer of the website. No Props because there shouldn't
 * be any configuration necessary.
 */
const Footer: FunctionComponent = () => (
  <footer>
    <div className={styles.wrapper}>
      <Container className="m-0">
        <Row>
          <Col xs={6} md={3} className="mb-5 mb-md-0">
            <FirstColumn />
          </Col>

          <Col xs={6} md={6} className="mb-5 mb-md-0">
            <SecondColumn />
          </Col>

          <Col xs={{ span: 8, offset: 2 }} md={{ span: 3, offset: 0 }}>
            <ThirdColumn />
          </Col>
        </Row>
      </Container>
    </div>
  </footer>
);

export default Footer;
