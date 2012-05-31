type file;
type imagefile;
type landuse;

# Define application program interfaces

app (landuse output) getLandUse (imagefile input, int sortfield)
{
  getlanduse @input sortfield stdout=@output ;
}

app (file output, file tilelist) analyzeLandUse
    (landuse input[], string usetype, int maxnum)
{
  analyzelanduse @output @tilelist usetype maxnum @filenames(input);
}

app (imagefile output) colorMODIS (imagefile input)
{
  colormodis @input @output;
}

app (imagefile output) assemble
    (file selected, imagefile image[], string webdir)
{
  assemble @output @selected @filename(image[0]) webdir;
}

app (imagefile grid) markMap (file tilelist) 
{
  markmap @tilelist @grid;
}

# Constants and command line arguments

int nFiles =      @toint(@arg("nfiles","1000"));
int nSelect =     @toint(@arg("nselect","12"));
string landType = @arg("landtype","urban");
string runID =    @arg("runid","modis-run");
string MODISdir=  @arg("modisdir","/home/wilde/bigdata/data/modis/2002");
string webDir =   @arg("webdir","/home/wilde/public_html/geo/");

string suffix=".tif";

# Input Dataset

imagefile geos[] <ext; exec="modismapper.py",
  f="h*", n=nFiles >; # site=site

# Compute the land use summary of each MODIS tile

landuse land[] <structured_regexp_mapper; source=geos, match="(h..v..)",
  transform=@strcat(runID,"/\\1.landuse.byfreq")>;

foreach g,i in geos {
    land[i] = getLandUse(g,1);
}

# Find the top N tiles (by total area of selected landuse types)

file topSelected<"topselected.txt">;
file selectedTiles<"selectedtiles.txt">;
(topSelected, selectedTiles) = analyzeLandUse(land, landType, nSelect);

# Mark the top N tiles on a sinusoidal gridded map

imagefile gridMap<"markedGrid.gif">;
gridMap = markMap(topSelected);

# Create multi-color images for all tiles

imagefile colorImage[] <structured_regexp_mapper;
          source=geos, match="(h..v..)", 
          transform="landuse/\\1.color.png">;

foreach g, i in geos {
  colorImage[i] = colorMODIS(g);
}

# Assemble a montage of the top selected areas

imagefile montage <single_file_mapper; file=@strcat(runID,"/","map.png") >; # @arg
montage = assemble(selectedTiles,colorImage,webDir);

# future args:

int selectHiThreshold;
int selectLowThreshold;
string upperLeftTile;
string lowerRightTile;
float imageSizes[];
string displayOptions;

