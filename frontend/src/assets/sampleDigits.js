/* Pure‑browser version: converts a 16×16 string of 0/1 characters into a data‑URL
   using an off‑screen Canvas element—NO external libraries needed. */

   function strToPNG(str) {
    const size = 16;
    const cvs = document.createElement("canvas");
    cvs.width = cvs.height = size;
    const ctx = cvs.getContext("2d");
    const imgData = ctx.createImageData(size, size);
    for (let i = 0; i < str.length; i++) {
      const bit = str[i] === "1" ? 0 : 255; // black for 1, white for 0
      imgData.data.set([bit, bit, bit, 255], i * 4);
    }
    ctx.putImageData(imgData, 0, 0);
    return cvs.toDataURL();
  }
  
  // minimal digit set – pad to 256 chars (16×16) for each digit
  const raw = {
    zero:   "000111100001000100010001000100010001000100011110000".padEnd(256, "0"),
    one:    "000010000001100000010000001000000100000011100000".padEnd(256, "0"),
    two:    "001111000010001000000010000001000010000100011111".padEnd(256, "0"),
    three:  "001111000010001000000110000000010000100001111000".padEnd(256, "0"),
  };
  
  export const digits = Object.fromEntries(
    Object.entries(raw).map(([k, v]) => [k, strToPNG(v)])
  );


  