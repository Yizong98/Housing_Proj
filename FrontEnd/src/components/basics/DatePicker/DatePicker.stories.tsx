import React, { ComponentProps } from 'react';
import { Story } from '@storybook/react';
import DatePicker from './DatePicker';

export default {
  title: 'DatePicker',
  component: DatePicker,
};

const Template: Story<ComponentProps<typeof DatePicker>> = (args) => (
  <DatePicker {...args} />
);

export const Default = Template.bind({});
