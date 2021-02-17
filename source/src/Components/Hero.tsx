import React from 'react'
import logo from '../Images/fortran_logo.png'

export default function Hero(){
    return(
        <div className="relative flex flex-col items-center justify-center min-h-screen bg-white bg-cover min-w-screen">
            <div
                className="flex flex-col flex-col-reverse items-center justify-center p-10 mx-auto lg:flex-row lg:max-w-6xl lg:p-0">
                <div className="relative w-full pr-10 rounded-lg cursor-pointer md:w-2/3 lg:w-1/2 group">
                    <div className="relative rounded-md">
                        <img src={logo}
                            className="z-10 object-cover w-full h-full"/>
                    </div>
                </div>
                <div
                    className="container relative z-20 flex flex-col w-full px-5 pr-12 mb-16 text-2xl text-gray-700 lg:w-1/2 sm:px-0 md:px-10 sm:items-center lg:items-start lg:mb-0">
                    <h1
                        className="relative z-20 font-sans text-4xl font-extrabold leading-none text-black sm:text-5xl xl:text-6xl sm:text-center lg:text-left">
                        <span className="relative">
                            <span
                                className="absolute bottom-0 left-0 inline-block w-full h-4 mb-1 -ml-1 transform -skew-x-3 bg-primary-200"></span>
                            <span className="relative">Package Manager</span>
                        </span>
                        <span className="relative block text-primary">Formula.</span>
                    </h1>
                    <p className="relative z-20 block mt-6 text-base text-gray-500 xl:text-lg sm:text-center lg:text-left">Coming soon...</p>
                    <div className="relative flex items-center mt-10">
                        <code>$ pip install formulapm</code>
                    </div>
                </div>
            </div>
        </div>
    )
}