import React from 'react';
import axios from 'axios';
import { Formik } from 'formik';
import { Image, Heading } from "@chakra-ui/core";
import Man from '../media/coolblackguy.jpg'

function Prelaunch(props) {

    const submitEmail = async (values, actions) =>{
        const url = "http://localhost:8000/";
        const formData = new FormData();
        formData.append('email', values.email);
        try{
            await axios.post(url, formData);
        }catch(response){
            const data = response.response.data;
            console.log(data);
        }
        console.log(
            "submitted " + values.email
        );
    }

    return (
        <div className="bg-gray-200 h-screen pt-6 flex flex-col relative text-blue-600">
            <div className="text-center h-screen bg-gray-200 flex flex-col mt-6 md:mt-12">
                <Heading className="p-2 z-20 mt-12">HELP ME THIS SUCKS SO MUCH!</Heading>
                <div className="flex flex-col md:flex-row md:mt-12">
                    <div className="z-20 md:flex md:flex-row md:w-2/3 md:mx-auto md:my-6 md:text-xl">
                        <div>
                        <Image className="mx-auto
						my-1 absolute md:static left-0 top-0 -mt-2 md:m-0 md:mb-" src="https://via.placeholder.com/160x60?text=Our+Logo" />

                        <div className="static w-8/12 md:w-1/2 mt-8 mx-auto md:m-0">
                            <p className="">Yo this is some copy text.
                            It's place is to fill space
                            until I figure out what to put here.
                            This and CSS are like my least favorite
                            things to do. I hate this crap.
                            Lorem ipsum I don't give a damn.
                        	</p>

                            <Formik
                                initialValues={{ email: '' }}
                                onSubmit={submitEmail}
                            >
                                {({
                                    handleSubmit,
                                    values,
                                    handleChange
                                }) =>
                                    <form onSubmit={handleSubmit} className="mt-6 md:mx-auto md:m-0" >
                                        <input className="p-1 rounded-l-sm w-8/12"
                                            type="email"
                                            name="email"
                                            value={values.email}
                                            onChange={handleChange}
                                        />
                                        <button className="bg-gradient-to-r from-teal-300 to-blue-500 p-1 rounded-r-sm text-red-100" type="submit">
                                            Submit
                            </button>
                                    </form>}
                            </Formik>
                        </div>
                        </div>
                        <img className="hidden md:block md:w-1/2" src={Man} />
                    </div>
                    <img className=" m-auto w-full h-screen inset-0 -z-20 absolute" src={Man} />
                </div>
            </div>
        </div>

    );
}

export default Prelaunch;