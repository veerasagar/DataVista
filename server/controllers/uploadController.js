import fs from "fs";
import csv from "csv-parser";

export const processCSVFile = (filePath) => {
  return new Promise((resolve, reject) => {
    const transactions = [];

    fs.createReadStream(filePath)
      .pipe(csv())
      .on("data", (row) => transactions.push(row))
      .on("end", () => resolve(transactions))
      .on("error", (error) => reject(error));
  });
};
