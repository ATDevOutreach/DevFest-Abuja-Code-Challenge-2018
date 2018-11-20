

new Vue({
    el: "#root",
    data:{
        title: "Admin Dashboard",
        orders:[
            {name:"John Bull", description:"Jollof Rice", address:"Chanchaga, Minna", telephone:"08031234567", open:true},
            {name:"Ibrahim Audu", description:"Tuwo Masara and Egusi Soup", address:"Bosso, Minna", telephone:"08085645678", open:true},
            {name:"Sani Shehu", description:"Eba and Egusi Soup", address:"Gidan Kwano, Minna", telephone:"08082345686", open:true},
            {name:"Habiba Salihu", description:"Tuwo Masara and Egusi Soup", address:"Chanchaga, Minna", telephone:"08082343478", open:true}

        ]
    },
    created(){
        var pusher = new Pusher('78d1e4b17078c3e0bde9',{
            cluster:'eu',
            encrypted:true
        })
        var channel = pusher.subscribe('orders')
        channel.bind('customerOrder', (data) => {
            console.log(data)
            this.orders.push(data)
        })
    },
    methods:{
        // close completed order
        close(orderToClose){
            if ( confirm('Are you sure you want to close this order?') === true){
                this.orders = this.orders.map(order => {
                    if(order.name !== orderToClose.name && order.description !== orderToClose.description){
                        return order;
                    }
                    const change = {
                        open: !order.open
                    }
                    return change;
                })
            } 
        }
    }
})