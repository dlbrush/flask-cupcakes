$(async function() {

    async function listCupcakes() {
        const cupcakes = await getCupcakes();
        const $list = $('#cupcakes');
        $list.empty()
        for (const cupcake of cupcakes) {
            $list.append(makeCupcakeLI(cupcake))
        }
    };

    async function handleSubmit(evt) {
        evt.preventDefault();
        const data = {
            flavor: $('#flavor').val(),
            size: $('#size').val(),
            rating: $('#rating').val(),
            image: $('#image').val()
        };
        await postCupcake(data);
        await listCupcakes();
    };

    function makeCupcakeLI(cupcake) {
        return `<li>
                    <img src="${cupcake.image}"/>
                    <ul>
                        <li>Flavor: ${cupcake.flavor}</li>
                        <li>Size: ${cupcake.size}</li>
                        <li>Rating: ${cupcake.rating}</li>
                    </ul>
                </li>`
    };

    async function getCupcakes() {
        const response = await axios.get('/api/cupcakes');
        return response.data.cupcakes;
    };

    async function postCupcake(data) {
        const response = await axios.post('/api/cupcakes', data);
    };

    await listCupcakes()
    $('#add-cupcake').on('submit', handleSubmit);
});