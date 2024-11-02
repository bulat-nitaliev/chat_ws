<template>
    <div>
        <row>
            <col span="4" xl="2" class="rooms-list">
                <button @click="addRoom">Создать комнату</button>
                <div v-for="room in rooms" :key="room.id">
                    <h3 @click="openDialog(room.id)">{{room.creator.username}}</h3>
                    <small>{{room.date}}</small>
                </div>
            </col>
            <slot></slot>
        </row>
    </div>
</template>

<script>
import $api from '@/http'

    export default {
        name: "Room",
        data() {
            return {
                rooms: '',
            }
        },
        created() {
            // $.ajaxSetup({
            //     headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
            // });
            // this.loadRoom()
        },
        methods: {
            // Загружаю список комнат
            async loadRoom() {
                const response = await $api.get('api/room/')
                this.rooms = response.data.data        
                   
            },
            openDialog(id) {
                this.$router.push({name: 'dialog', params: {id: id}})
            },
            // Создание комнаты
            async addRoom() {
                const response = await $api.post("api/room/")
                this.loadRoom()
            }
        }
    }
</script>

<style scoped>
    h3 {
        cursor: pointer;
    }

    .rooms-list {
        margin: 0 10px 0 0;
        box-shadow: 1px 4px 5px #848181;
    }
</style>