import React, { useState, FunctionComponent } from 'react';
import { DateRangePicker } from 'react-dates';
import moment from 'moment';
import 'react-dates/initialize';
import 'react-dates/lib/css/_datepicker.css';
import styles from './DatePicker.module.scss';
import { miscIcons } from '@icons';
import cn from 'classnames';

const PrevArrow = () => (
  <miscIcons.largeLeftArrow
    className={cn(styles.arrow, styles.left, styles.mounted)}
  />
);

const NextArrow = () => (
  <miscIcons.largeRightArrow
    className={cn(styles.arrow, styles.right, styles.mounted)}
  />
);

const RangeArrow = () => (
  <miscIcons.largeRightArrow className={cn(styles.arrow)} />
);

type CalendarDate = moment.Moment | null;

const DatePicker: FunctionComponent = () => {
  const [dateRange, setDateRange] = useState<{
    startDate: CalendarDate;
    endDate: CalendarDate;
  }>({
    startDate: null,
    endDate: null,
  });
  const [focus, setFocus] = useState<'startDate' | 'endDate' | null>(null);

  const { startDate, endDate } = dateRange;

  return (
    <DateRangePicker
      startDatePlaceholderText="Start"
      startDate={startDate}
      onDatesChange={setDateRange}
      endDatePlaceholderText="End"
      endDate={endDate}
      numberOfMonths={1}
      displayFormat="MMM D"
      showClearDates={true}
      focusedInput={focus}
      keepOpenOnDateSelect={true}
      onFocusChange={setFocus}
      startDateId="startDate"
      endDateId="endDate"
      customArrowIcon={<RangeArrow />}
      minimumNights={0}
      navPrev={<PrevArrow />}
      navNext={<NextArrow />}
    />
  );
};

export default DatePicker;
