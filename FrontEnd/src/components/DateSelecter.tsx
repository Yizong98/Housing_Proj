import React, { useState } from 'react';
import { DateRangePicker } from 'react-dates';
import moment from 'moment';
import 'react-dates/initialize';
import 'react-dates/lib/css/_datepicker.css';

function Datepicker() {
  const [dateRange, setdateRange] = useState<{
    startDate: moment.Moment | null;
    endDate: moment.Moment | null;
  }>({
    startDate: null,
    endDate: null,
  });
  const [focus, setFocus] = useState<'startDate' | 'endDate' | null>(null);

  const { startDate, endDate } = dateRange;

  const handleOnDateChange = ({
    startDate,
    endDate,
  }: {
    startDate: moment.Moment | null;
    endDate: moment.Moment | null;
  }) => {
    if (startDate !== null) {
      console.log(startDate.unix(), 'timestamp');
    }
    setdateRange({ startDate, endDate });
  };
  return (
    <DateRangePicker
      startDatePlaceholderText="Start"
      startDate={startDate}
      onDatesChange={handleOnDateChange}
      endDatePlaceholderText="End"
      endDate={endDate}
      numberOfMonths={1}
      displayFormat="MMM D"
      showClearDates={true}
      focusedInput={focus}
      onFocusChange={(focus) => setFocus(focus)}
      startDateId="startDateMookh"
      endDateId="endDateMookh"
      minimumNights={0}
    />
  );
}

export default Datepicker;
