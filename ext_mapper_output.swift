type file;

file inputfiles1[] <ext;exec="mapper.py",filename=@arg("in1")>;
file inputfiles2[] <ext;exec="mapper.py",filename=@arg("in2")>;

app (file o) cat (file i1, file i2)
{
	cat @i1 @i2 stdout=@o;
}

foreach i, j in inputfiles1 {
	string name = @strcat(@arg("out"), j, ".txt");
	trace(name);
	file c<ext;exec="postmapper.py",filename= name,owner=@arg("owner")>;
	c = cat(i, inputfiles2[j]);
}
