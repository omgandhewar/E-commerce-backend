// async function loadproduct(){
//     const response=await fetch(
//         "http://127.0.0.1:5000/products/104"
//     );
//     const data = await response.json();
//     console.log(data);
// }

document.getElementById("id1").addEventListener("submit",async function(event){

    event.preventDefault();

    let email=document.getElementById("email").value;
    let password=document.getElementById("password").value;

    const response = await fetch(
        "http://127.0.0.1:5000/login",
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                email:email,
                password:password
            })
        }
    );

    const data = await response.json();
    console.log(data);
})

// async function login() {

//     const response = await fetch(
//         "http://127.0.0.1:5000/login",
//         {
//             method:"POST",
//             headers:{
//                 "Content-Type":"application/json"
//             },
//             body:JSON.stringify({
//                 email:email,
//                 password:password
//             })
//         }
//     );

//     const data = await response.json();
//     console.log(data);
// }