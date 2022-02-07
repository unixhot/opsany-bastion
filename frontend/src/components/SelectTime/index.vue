<template>
    <div>
        <div class="boxhelp">
            <div>
                <div class="allowBox"></div>
                <div>{{ allowText }}</div>
            </div>
            <div>
                <div class="disabledBox" :style="{ background: disabledColor }"></div>
                <div>{{ disabledText }}</div>
            </div>
        </div>

        <div v-for="week in weekList" class="container">
            <span class="week_name" @click="clickWeek(week)">{{ week.name }}</span>
            <span
                v-for="(time, timeIndex) in 24"
                class="timebox"
                @click="clickTimeBox(week, timeIndex)"
                :style="{ background: week.activeTime.includes(timeIndex) ? '#0ba360' : disabledColor }"
            >
            </span>
            <a-select mode="multiple" v-model="week.activeTime" hidden>
                <a-select-option v-for="(time, timeIndex) in 24" :key="timeIndex" :value="timeIndex">
                    {{ timeIndex }}
                </a-select-option>
            </a-select>
        </div>
        <div class="timecountbox">
            <span v-for="(time, timeIndex) in 24" class="timecount" @click="clickTime(timeIndex)">
                {{ timeIndex }}
            </span>
        </div>
        <div>
            <a-button type="link" @click="allCheck">全选</a-button>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        value: {
            type: Array,
            default: () => {
                return []
            },
        },
        disabledColor: {
            type: String,
            default: '#ffffff',
        },
        allowText: {
            type: String,
            default: '允许',
        },
        disabledText: {
            type: String,
            default: '禁止',
        },
    },
    model: {
        prop: 'value',
        event: 'change',
    },
    methods: {
        clickTimeBox(week, timeIndex) {
            if (week.activeTime.includes(timeIndex)) {
                const index = week.activeTime.findIndex((it) => it == timeIndex)
                week.activeTime.splice(index, 1)
            } else week.activeTime.push(timeIndex)
            this.emitWeekList()
        },
        allCheck() {
            const allCheck = this.weekList.every((item) => item.activeTime.length == 24)
            this.weekList.forEach((item) => {
                if (allCheck) {
                    item.activeTime = []
                } else item.activeTime = Array.from({ length: 24 }, (item, index) => index)
            })
            this.emitWeekList()
        },
        clickWeek(week) {
            const activeTime = week.activeTime.length == 24 ? [] : Array.from({ length: 24 }, (item, index) => index)
            this.$set(week, 'activeTime', activeTime)
            this.emitWeekList()
        },
        clickTime(timeIndex) {
            const alreadyCheckTime = this.weekList
                .map((item) => {
                    return item.activeTime.find((it) => it == timeIndex)
                })
                .filter((item) => item != undefined)
            const isCheckAllTime = alreadyCheckTime.length == this.weekList.length
            if (isCheckAllTime) {
                this.weekList.forEach((item) => {
                    const index = item.activeTime.findIndex((it) => it == timeIndex)
                    item.activeTime.splice(index, 1)
                })
                this.emitWeekList()
            } else {
                this.weekList.forEach((item) => {
                    !item.activeTime.includes(timeIndex) && item.activeTime.push(timeIndex)
                    item.activeTime.sort((a, b) => a - b)
                })
                this.emitWeekList()
            }
        },
        emitWeekList() {
            const weekList = this.weekList.map((item) => {
                return {
                    week: item.key,
                    time: item.activeTime.sort((a, b) => a - b),
                }
            })
            this.$emit('change', weekList)
        },
    },
    computed: {
        weekList() {
            const weekList = [
                { key: 1, name: '周一', activeTime: [] },
                { key: 2, name: '周二', activeTime: [] },
                { key: 3, name: '周三', activeTime: [] },
                { key: 4, name: '周四', activeTime: [] },
                { key: 5, name: '周五', activeTime: [] },
                { key: 6, name: '周六', activeTime: [] },
                { key: 7, name: '周日', activeTime: [] },
            ]
            this.value.forEach((item) => {
                const week = weekList.find((it) => it.key == item.week)
                week.activeTime = item.time
            })
            return weekList
        },
    },
    mounted() {
        // this.allCheck()
    },
}
</script>
<style scoped lang='less'>
.boxhelp {
    display: flex;
    margin-bottom: 10px;
    > div {
        display: flex;
        align-items: center;
        &:nth-child(2) {
            margin-left: 20px;
        }
    }
    .allowBox {
        display: inline-block;
        width: 18px;
        height: 18px;
        background: #0ba360;
        border-color: 1px solid #0ba360;
        margin-right: 8px;
    }
    .disabledBox {
        display: inline-block;
        width: 18px;
        height: 18px;
        border: 1px solid #eeeeee;
        margin-right: 8px;
    }
}
.container {
    display: flex;
    align-items: center;
    line-height: none !important;
    margin: 0;
    padding: 0;
    .week_name {
        display: inline-block;
        width: 30px;
        margin-right: 5px;
        cursor: pointer;
    }
    .timebox {
        width: 20px;
        height: 20px;
        border: 1px solid #eeeeee;
        margin-left: 1px;
        margin-bottom: 1px;
        &:hover {
            border-color: #0ba360;
        }
        transition: all 0.1s;
    }
}
.timecountbox {
    margin-left: 35px;
    margin-top: 5px;
    .timecount {
        display: inline-block;
        width: 20px;
        height: 20px;
        margin-left: 1px;
        text-align: center;
        cursor: pointer;
    }
}
</style>