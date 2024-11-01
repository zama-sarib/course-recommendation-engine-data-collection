#!/bin/bash
echo "Deleting existing Files from Dataset directory"
rm -rf ./Dataset/*

kaggle datasets download thedevastator/udemy-courses-revenue-generation-and-course-anal 
kaggle datasets download andrewmvd/udemy-courses
kaggle datasets download jilkothari/finance-accounting-courses-udemy-13k-course
mv ./udemy-courses-revenue-generation-and-course-anal.zip ./udemy-courses.zip ./finance-accounting-courses-udemy-13k-course.zip ./Dataset/