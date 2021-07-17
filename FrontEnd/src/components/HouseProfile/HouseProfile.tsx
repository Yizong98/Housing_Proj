import React, { FunctionComponent } from 'react';
import { useLandlordRoomData } from '@hooks';
import GeneralInfo from './GeneralInfo/GeneralInfo';
import PlaceDetails from './PlaceDetails/PlaceDetails';
import ApplicationDetails from './ApplicationDetails/ApplicationDetails';
import styles from './HouseProfile.module.scss';
import { Head } from '@basics';

interface HouseProfileProps {
  roomId: number;
}

const HouseProfile: FunctionComponent<HouseProfileProps> = ({ roomId }) => {
  const { data, error } = useLandlordRoomData(roomId);

  if (error) {
    return <div>Error occurred!</div>; // TODO handle error in a different way
  }

  if (!data) {
    return (
      <>
        <Head title="Loading Place..." />
        <div>Loading...</div>; // TODO add a loader
      </>
    );
  }

  const { address, name, distance, images } = data;

  const slideShowItems = images.map((url) => ({
    src: url,
    alt: `${name} , ${address}}`,
  }));

  return (
    <>
      <Head title={name} />

      <div className="px-md-0 px-3">
        <div className={styles.section}>
          <GeneralInfo
            images={slideShowItems}
            address={address}
            distance={distance}
            name={name}
          />
        </div>

        <div className={styles.section}>
          <PlaceDetails roomId={roomId} />
        </div>

        <ApplicationDetails roomId={roomId} />
      </div>
    </>
  );
};

export default HouseProfile;
