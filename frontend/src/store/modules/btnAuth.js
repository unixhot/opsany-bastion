const btnAuth = {
    state: {
        btnAuth: {},
    },
    mutations: {
        SET_BTNAUTH: (state, data) => {
            state.btnAuth = data
        }
    },
    actions: {
        GenerateBtnAuth({ commit },data) {
            commit('SET_BTNAUTH', data)
        }
    }
}

export default btnAuth
