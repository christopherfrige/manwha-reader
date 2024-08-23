import { mount } from '@vue/test-utils';
import DatePostedLabel from '../../components/chapter/DatePostedLabel.vue';

describe('DatePostedLabel', () => {
  it('displays the correct label for a recent post', () => {
    const postedAt = new Date().toISOString().slice(0, -1);
    const wrapper = mount(DatePostedLabel, {
      propsData: { postedAt },
    });
    expect(wrapper.text()).toContain('Agora');
  });

  it('displays the correct label for a post made a few minutes ago', () => {
    const now = new Date();
    const postedAt = new Date(now - 5 * 60 * 1000).toISOString().slice(0, -1); // 5 minutes ago
    const wrapper = mount(DatePostedLabel, {
      propsData: { postedAt },
    });
    expect(wrapper.text()).toContain('5 minutos atrás');
  });

  it('displays the correct label for a post made a few hours ago', () => {
    const now = new Date();
    const postedAt = new Date(now - 5 * 60 * 60 * 1000).toISOString().slice(0, -1); // 5 hours ago
    const wrapper = mount(DatePostedLabel, {
      propsData: { postedAt },
    });
    expect(wrapper.text()).toContain('5 horas atrás');
  });

  it('displays the correct label for a post made yesterday', () => {
    const now = new Date();
    const yesterday = new Date(now - 24 * 60 * 60 * 1000); // Yesterday
    const postedAt = yesterday.toISOString().slice(0, -1);
    const wrapper = mount(DatePostedLabel, {
      propsData: { postedAt },
    });
    expect(wrapper.text()).toContain('Ontem');
  });

  it('displays the correct label for a post made several days ago', () => {
    const postedAt = new Date('2023-01-01 12:00:00').toISOString(); // Example date
    const wrapper = mount(DatePostedLabel, {
      propsData: { postedAt },
    });
    expect(wrapper.text()).toContain('1 de Janeiro de 2023');
  });
});
