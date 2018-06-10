# this file gets sourced at the start of the app
# after the heroku config vars.

IMP_BIN="$HOME"/impbin
REF_PANEL="$HOME"/1000GP_Phase3
DATA_DIR="$HOME"/data
REF_FA="$HOME"/hg19
OUT_DIR="$HOME"/genipe_output

if [ ! -d "$IMP_BIN" ]; then
  mkdir $IMP_BIN

  echo DOWNLOADING IMPUTE2...
  wget https://mathgen.stats.ox.ac.uk/impute/impute_v2.3.2_x86_64_static.tgz
  tar -xvzf impute_v2.3.2_x86_64_static.tgz
  mv impute_v2.3.2_x86_64_static/impute2 $IMP_BIN/impute2

  echo DOWNLOADING PLINK...
  wget https://www.cog-genomics.org/static/bin/plink180528/plink_linux_x86_64.zip
  unzip plink_linux_x86_64.zip
  mv plink $IMP_BIN/plink

  echo DOWNLOADING SHAPEIT...
  wget https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.v2.r837.GLIBCv2.12.Linux.static.tgz
  tar -xvzf shapeit.v2.r837.GLIBCv2.12.Linux.static.tgz
  mv bin/shapeit $IMP_BIN/shapeit
fi

if [ ! -d "$REF_PANEL" ]; then
  echo DOWNLOADING 1kG HAPLOTYPES...
  wget https://mathgen.stats.ox.ac.uk/impute/1000GP_Phase3.tgz
  tar -xvzf 1000GP_Phase3.tgz
  cd
fi

if [ ! -d "$REF_FA" ]; then
  echo DOWNLOADING HG19...
  wget -P $REF_FA http://statgen.org/wp-content/uploads/Softwares/genipe/supp_files/hg19.fasta

# this is where the OH user data will exist
mkdir $DATA_DIR