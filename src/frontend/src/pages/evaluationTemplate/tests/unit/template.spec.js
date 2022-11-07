import { shallowMount, createLocalVue, mount } from "@vue/test-utils";
import Vue from "vue";
import Vuex from "vuex";
import vuexstore from "@/store/modules/probation";
import CriteriaItem from "@/pages/evaluationTemplate/myEvaluationTemplate/criteriaItemComponent.vue";
import AddTemplate from "@/pages/evaluationTemplate/myEvaluationTemplate/addNewEvaluationTemplate.vue";
import ListTemplate from "@/pages/evaluationTemplate/myEvaluationTemplate/myEvaluationTemplate.vue";
import ElementUI from "element-ui";

describe("criteriaItemComponent.vue", () => {
  it("renders props.criterias props.isAdd props.type_item when passed", () => {
    const criterias = [1, 2, 3];
    const isAdd = true;
    const type_item = "competencies";

    const wrapper = shallowMount(
      CriteriaItem,
      {
        propsData: { criterias, isAdd, type_item },
      },
      Vue.use(ElementUI)
    );

    expect(wrapper.props().criterias).toEqual([1, 2, 3]);
    expect(wrapper.props().isAdd).toBe(true);
    expect(wrapper.props().type_item).toBe("competencies");
  });
});

describe("addNewEvaluationTemplate.vue", () => {
  const localVue = createLocalVue();
  let store;
  localVue.use(Vuex);
  localVue.use(ElementUI);

  beforeEach(() => {
    store = new Vuex.Store(vuexstore);
  });

  it("change value when submitted", async () => {
    const wrapper = mount(AddTemplate, { store, localVue });
    wrapper.setData({
      formEvaluationTemplate: {
        name: "Evaluation Template Builder",
        office: 1,
        competencies: [
          {
            competence: "com 1",
            assessor_roles: [{ assessor_role: "Self-evaluation" }],
          },
        ],
        overall_comments: [
          {
            term: "overall",
            assessor_roles: [{ overall_comment_role: "Self-evaluation" }],
          },
        ],
      },
    });
    expect(wrapper.vm.value).toBe(0);
    await wrapper.find("#btn-submit").trigger("click");
    expect(wrapper.vm.value).toBe(1);
  });

  it("redirect to /evaluation-form-templates/ when clicking on discard button", async () => {
    const wrapper = mount(AddTemplate, { store, localVue });
    Object.defineProperty(window, "location", {
      value: {
        href: "http://localhost/evaluation-form-templates/new-evaluation-form-template",
      },
      configurable: true,
    });
    await wrapper.find("#btn-discard").trigger("click");
    expect(window.location.href).toBe("/evaluation-form-templates");
  });
});

describe("myEvaluationTemplate.vue", () => {
  const localVue = createLocalVue();
  let store;
  localVue.use(Vuex);
  localVue.use(ElementUI);

  beforeEach(() => {
    store = new Vuex.Store(vuexstore);
  });

  it("redirect to /new-evaluation-form-template/ when clicking on add button", async () => {
    const wrapper = await mount(ListTemplate, { store, localVue });
    Object.defineProperty(window, "location", {
      value: {
        href: "http://localhost/evaluation-form-templates",
      },
      configurable: true,
    });
    await wrapper.find("#btn-add-template").trigger("click");
    expect(window.location.href).toBe(
      "/evaluation-form-templates/new-evaluation-form-template"
    );
  });
});
