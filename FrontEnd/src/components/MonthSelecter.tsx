import React, { useState } from 'react';
import { DateRangePicker } from 'react-dates';
import moment from 'moment';
import 'react-dates/initialize';
import 'react-dates/lib/css/_datepicker.css';

function RenderMonthElement(props: {
  month: moment.Moment;
  onMonthSelect: (currentMonth: moment.Moment, newMonth: string) => void;
  onYearSelect: (currentYear: moment.Moment, newYear: string) => void;
  isVisible: boolean;
}): React.ReactNode {
  return (
    <div>
      <div>
        <select
          value={props.month.month()}
          onChange={(e) => props.onMonthSelect(props.month, e.target.value)}
        >
          {moment.months().map((label, value) => (
            <option value={value}>{label}</option>
          ))}
        </select>
      </div>
      <div>
        <select
          value={props.month.year()}
          onChange={(e) => props.onYearSelect(props.month, e.target.value)}
        >
          <option value={moment().year() - 1}>{moment().year() - 1}</option>
          <option value={moment().year()}>{moment().year()}</option>
          <option value={moment().year() + 1}>{moment().year() + 1}</option>
        </select>
      </div>
    </div>
  );
}

function MonthSelecter() {
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
      displayFormat="MMM D Y"
      showClearDates={true}
      focusedInput={focus}
      onFocusChange={(focus) => setFocus(focus)}
      startDateId="startDateMookh"
      endDateId="endDateMookh"
      minimumNights={0}
      renderMonthElement={RenderMonthElement}
    />
  );
}

export default MonthSelecter;
