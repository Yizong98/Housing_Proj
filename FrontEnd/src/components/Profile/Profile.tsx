import React, { useState, FunctionComponent, useEffect } from 'react';
import { Col, Container, Form, Row } from 'react-bootstrap';
import Image from 'react-bootstrap/Image';
import { SchoolYear, majors } from '@constants';
import { Dropdown, Input, ToggleGroup, Button, Head } from '@basics';
import { profileIcons } from '@icons';
import styles from './Profile.module.scss';
import cn from 'classnames';
import { useUser } from '@hooks';
import { User } from '@models';
import { useRouter } from 'next/router';
import { TriggerPageView } from '@components/ga';

const phoneFormat = (phone: string, previousPhone: string) => {
  const phoneRegex = /\d+/;
  const charArray = [];
  const limit = 14;
  let i;
  for (i = 0; i < Math.min(phone.length, limit); i++) {
    if (phone[i].match(phoneRegex)) {
      charArray.push(phone[i]);
    }
  }
  if (
    previousPhone.length > phone.length && // if it is a delete operation
    phone.length > 0 && // if it is non empty
    !previousPhone[previousPhone.length - 1].match(phoneRegex)
  ) {
    charArray.pop();
  }
  const bracket = charArray.length >= 3;
  const space = charArray.length > 3;
  const horizontal = charArray.length > 6;
  if (horizontal) {
    charArray.splice(6, 0, '-');
  }
  if (space) {
    charArray.splice(3, 0, ' ');
  }
  if (bracket) {
    charArray.splice(0, 0, '(');
    charArray.splice(4, 0, ')');
  }
  return charArray.join('');
};

const Profile: FunctionComponent = () => {
  const { data: user, isLoading, updateUser } = useUser();
  const [userDraft, setUserDraft] = useState<User | undefined>(
    user.isLoggedIn ? user : undefined,
  );
  const [isNotEditing, setisNotEditing] = useState(true);
  const [viewMyPosts, setViewMyPosts] = useState(false);
  const router = useRouter();

  // need to update user draft when user data is retrieved
  useEffect(() => {
    if (!isLoading && user.isLoggedIn) {
      // do not include isLoggedIn in userDraft
      setUserDraft(user);
    }
  }, [isLoading]);

  // GA page tracking
  TriggerPageView('/profile');

  if (isLoading) {
    return <div>Loading user data...</div>;
  }

  // if not logged, redirect to housing page
  if (!user.isLoggedIn) {
    router.push('/housing');
    return <div>Not logged in, redirecting to browse house posts!</div>;
  }

  if (!userDraft) {
    return <div>Loading user draft...</div>;
  }

  return (
    <>
      <Head title="Profile" />

      <Container className={styles.wrapper}>
        <Row className={styles.content}>
          <Col md={2}>
            <div
              className={cn(styles.titleSelected, {
                [styles.selectOff]: viewMyPosts,
              })}
              onClick={() => setViewMyPosts(false)}
            >
              <span
                className={cn(styles.divider, {
                  [styles.dividerOff]: viewMyPosts,
                })}
              ></span>
              <div className={styles.selectItem}>Profile</div>
            </div>
          </Col>

          <Col>
            <div className={`my-4 px-4 ${styles.middleSection}`}>
              <Row className={styles.userStaticInfo}>
                <Col md={2}>
                  <Image
                    src={userDraft.profilePhoto}
                    roundedCircle
                    className={styles.icon}
                  />
                </Col>

                <Col md={3}>
                  <div className={styles.name}>{userDraft.name}</div>
                  {isNotEditing ? (
                    <div className={styles.UserIdentifier}>
                      {userDraft.phone}
                    </div>
                  ) : (
                    <Form.Control
                      type="text"
                      value={userDraft.phone}
                      className={styles.phoneNum}
                      onChange={(event) => {
                        console.log(user, 'hello');
                        const previousPhone = userDraft.phone;
                        setUserDraft({
                          ...userDraft,
                          phone: phoneFormat(event.target.value, previousPhone),
                        });
                      }}
                    />
                  )}
                </Col>

                <Col md={3}>
                  <div className={styles.verified}>
                    <profileIcons.tickMark />
                    <span className={styles.smallText}>
                      UCSD Email Verified
                    </span>
                  </div>
                  <div className={styles.UserIdentifier}>{userDraft.email}</div>
                </Col>

                <Col className={styles.controlButton}>
                  {isNotEditing ? (
                    <Button
                      size="secondary"
                      variant="outline"
                      onClick={() => setisNotEditing(false)}
                      icon={{ icon: profileIcons.edit }}
                    >
                      Edit
                    </Button>
                  ) : (
                    <Button
                      size="secondary"
                      icon={{ icon: profileIcons.save }}
                      onClick={() => {
                        updateUser(userDraft);
                        setisNotEditing(true);
                      }}
                    >
                      Save
                    </Button>
                  )}
                </Col>
              </Row>

              <div className={styles.textInfo}>
                <Form.Row>
                  <Form.Group as={Col} controlId="profileSchoolYear">
                    <Form.Label className={styles.label}>
                      School year
                    </Form.Label>
                    <Form.Row>
                      <ToggleGroup
                        singleSelect
                        content={Object.values(SchoolYear)}
                        initialSelected={userDraft.schoolYear}
                        readOnly={isNotEditing}
                        onSelect={({ label }) => {
                          setUserDraft({
                            ...userDraft,
                            schoolYear: label as SchoolYear,
                          });
                        }}
                      />
                    </Form.Row>
                  </Form.Group>
                </Form.Row>

                <Form.Row className={styles.dropdown}>
                  <Form.Group
                    as={Col}
                    controlId="profileMajor"
                    className="pl-0"
                  >
                    <Form.Label className={styles.label}>Major</Form.Label>
                    {!isNotEditing ? (
                      <Dropdown
                        options={majors}
                        label=""
                        initialSelected={userDraft.major}
                        placeholder="Major"
                        onSelect={(s) => {
                          setUserDraft({
                            ...userDraft,
                            major: s || userDraft.major,
                          });
                        }}
                      />
                    ) : (
                      <Input
                        type="text"
                        value={userDraft.major}
                        readOnly
                        placeholder="Major"
                      />
                    )}
                  </Form.Group>
                </Form.Row>

                <Form.Row className={styles.bio}>
                  <Form.Group as={Col} controlId="profileBio" className="pl-0">
                    <Form.Label className={styles.label}>Short bio</Form.Label>
                    <Form.Control
                      readOnly={isNotEditing}
                      as="textarea"
                      className={styles.bioText}
                      type="text"
                      maxLength={600}
                      value={userDraft.description}
                      onChange={(event) =>
                        setUserDraft({
                          ...userDraft,
                          description: event.target.value,
                        })
                      }
                    />
                    <span className={styles.charCheck}>
                      {userDraft.description.length}/600
                    </span>
                  </Form.Group>
                </Form.Row>
              </div>
            </div>
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Profile;
