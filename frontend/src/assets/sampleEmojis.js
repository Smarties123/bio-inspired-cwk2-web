// Creates 32×32 monochrome emoji rasters that match backend format
import twemoji from "twemoji";

function emojiToPNG(char) {
  const size = 32;
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = "white";
  ctx.fillRect(0,0,size,size);

  const svg = twemoji.parse(char).match(/src="([^"]+)"/)[1];
  const img  = new Image();
  img.src = svg;
  return new Promise(res=>{
    img.onload = ()=>{
      ctx.drawImage(img, 0, 0, size, size);
      res(canvas.toDataURL());
    };
  });
}

export const emojis = {};   /* filled asynchronously in Controls; keeps code short */
["🙂","😂","😎","❤️","🚀"].forEach(async (e,i)=>{
  emojis[`emoji${i}`] = await emojiToPNG(e);
});
