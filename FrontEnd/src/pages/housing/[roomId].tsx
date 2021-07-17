import React, { useEffect, useState, FunctionComponent } from 'react';
import { HouseProfile } from '@components';
import { Head } from '@basics';
import { useRouter } from 'next/router';
import { TriggerPageView } from '@components/ga';

// parses the query parameter into a number (or undefined)
// TODO should show 404 type page if the roomid that is passed doesn't exist
const parseQueryParam = (params?: string | string[]) => {
  let roomIdString;
  if (typeof params === 'string') {
    roomIdString = params;
  } else {
    roomIdString = params ? params[0] : '';
  }

  const roomId = parseInt(roomIdString);
  return isNaN(roomId) ? undefined : roomId;
};

const Housing: FunctionComponent = () => {
  const router = useRouter();
  const [roomId, setRoomId] = useState<number | undefined>();

  // TODO potentially separate this into its own hook
  // this is needed because query in the router is not immediately defined
  useEffect(() => {
    if (!router.isReady) return;

    const roomId = parseQueryParam(router.query.roomId);
    setRoomId(roomId);

    TriggerPageView('housing/' + roomId?.toString());
  }, [router]);

  if (roomId) return <HouseProfile roomId={roomId} />;

  return <div>Loading...</div>;
};

export default Housing;
