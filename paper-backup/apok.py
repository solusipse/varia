import Image, ImageOps, ImageFont, ImageDraw, sys, math
from bitarray import bitarray

interval = 2

a4_width  = 690
a4_height = int(a4_width * 1.4142)

filename = 'gamepack.7z'

print("Opening file %s." % filename)
b = bitarray()
with open(filename, 'r') as f:
    b.fromfile(f)

print("Saving as bits array to out.txt.")
with open('out.txt', 'w+') as f:
    for a in b:
        f.write(str(int(a)))

print("Canvas:   " + str(a4_height*a4_width))
print("Data len: " + str(len(b)))

pages = int(math.ceil(len(b) / float(a4_height*a4_width)))
print("Creating %s pages..." % pages)

print("Used %i%% of space." % (int(len(b)/float(a4_height*a4_width)*100)/pages))

a4_width  *= interval
a4_height *= interval

# Calculate ppi
ppi = int(math.sqrt( a4_height*a4_height + a4_width*a4_width ) / 14)
print("PPI: %d." % ppi)

a = 0
for p in range(pages):
    img = Image.new("1", (a4_width,a4_height), "white")
    c = a
    for h in xrange(0,a4_height,interval):
        for w in xrange(0,a4_width,interval):
            if a >= len(b): break
            img.putpixel([w,h], not b[a])
            
            a += 1
    c = 0

    # TODO: fix this (eof)
    '''
    for i in range(8):
        if w >= a4_width:
            w  = 0
            h += 1
        img.putpixel([w+i,h], 0)
    '''

    # add border
    img = ImageOps.expand(img,border=2,fill="white")
    img = ImageOps.expand(img,border=2,fill="black")

    # move to bigger canvas
    out = Image.new("1", (a4_width+4,a4_height+8+12), "white")
    out.paste(img, (0,0))

    # add text
    drw = ImageDraw.Draw(out)
    drw.text( (5, a4_height+7), "File: %s, page: %i/%i, file size: %i B, "              \
        "page size: %i B, interval: %i, est. ppi: %i, width: %ipx, height: %ipx."       \
        % (filename, p + 1, pages, len(b)/8, a/8, interval, ppi, a4_width, a4_height) )

    out.save("out" + str(p) + ".bmp")
    print("Page %s saved to: out%s.bmp." % (str(p+1), str(p)))

print("Saved %i bytes. Input had %i bytes. %s" % (a/8, len(b)/8, "Success!" if a/8==len(b)/8 else "Something went wrong!") )
