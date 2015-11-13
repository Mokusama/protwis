﻿from django.db import models


class Structure(models.Model):
    protein_conformation = models.ForeignKey('protein.ProteinConformation')
    structure_type = models.ForeignKey('StructureType')
    pdb_code = models.ForeignKey('common.WebLink')
    state = models.ForeignKey('protein.ProteinState')
    publication = models.ForeignKey('common.Publication', null=True)
    ligands = models.ManyToManyField('ligand.Ligand', through='interaction.StructureLigandInteraction')
    protein_anomalies = models.ManyToManyField('protein.ProteinAnomaly')
    stabilizing_agents = models.ManyToManyField('StructureStabilizingAgent')
    preferred_chain = models.CharField(max_length=20)
    resolution = models.DecimalField(max_digits=5, decimal_places=3)
    publication_date = models.DateField()
    pdb_data = models.ForeignKey('PdbData', null=True) #allow null for now, since dump file does not contain.
    representative = models.BooleanField(default=False)


    def __str__(self):
        return self.pdb_code.index

    def get_preferred_chain_pdb(self):

        tmp = []
        for line in self.pdb_data.pdb.split('\n'):
            # http://www.wwpdb.org/documentation/file-format-content/format33/sect9.html#ATOM
            if (line.startswith('ATOM') or line.startswith('HET')) and line[21] == self.preferred_chain[0]:
                tmp.append(line)
        return '\n'.join(tmp)

    class Meta():
        db_table = 'structure'


class StructureModel(models.Model):
    protein = models.ForeignKey('protein.Protein')
    state = models.ForeignKey('protein.ProteinState')
    main_template = models.ForeignKey('structure.Structure')
    pdb = models.TextField()
    
    def __repr__(self):
        return '<HomologyModel: '+str(self.protein.entry_name)+' '+str(self.state)+'>'

    class Meta():
        db_table = 'structure_model'      


class StructureModelLoopTemplates(models.Model):
    homology_model = models.ForeignKey('structure.StructureModel')
    template = models.ForeignKey('structure.Structure')
    segment = models.ForeignKey('protein.ProteinSegment')
        
    class Meta():
        db_table = 'structure_model_loop_templates'
        
        
class StructureModelAnomalies(models.Model):
    homology_model = models.ForeignKey('structure.StructureModel')
    anomaly = models.ForeignKey('protein.ProteinAnomaly')
    reference = models.CharField(max_length=1)
    template = models.ForeignKey('structure.Structure')
    
    class Meta():
        db_table = 'structure_model_anomalies'
        
        
class StructureModelResidues(models.Model):
    homology_model = models.ForeignKey('structure.StructureModel')
    sequence_number = models.IntegerField()
    residue = models.ForeignKey('residue.Residue')
    rotamer = models.ForeignKey('structure.Rotamer')
    template = models.ForeignKey('structure.Structure')
    origin = models.CharField(max_length=15)
    segment = models.ForeignKey('protein.ProteinSegment')
    
    class Meta():
        db_table = 'structure_model_residues'


class StructureType(models.Model):
    slug = models.SlugField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta():
        db_table = "structure_type"


class StructureStabilizingAgent(models.Model):
    slug = models.SlugField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta():
        db_table = "structure_stabilizing_agent"


class PdbData(models.Model):
    pdb = models.TextField()

    def __str__(self):
        return self.pdb

    class Meta():
        db_table = "structure_pdb_data"


class Rotamer(models.Model):
    residue = models.ForeignKey('residue.Residue')
    structure = models.ForeignKey('structure.Structure')
    pdbdata = models.ForeignKey('PdbData')

    class Meta():
        db_table = "structure_rotamer"


class Fragment(models.Model):
    residue = models.ForeignKey('residue.Residue')
    ligand = models.ForeignKey('ligand.Ligand')
    structure = models.ForeignKey('structure.Structure')
    pdbdata = models.ForeignKey('PdbData')

    class Meta():
        db_table = "structure_fragment"


class StructureSegment(models.Model):
    structure = models.ForeignKey('Structure')
    protein_segment = models.ForeignKey('protein.ProteinSegment')
    start = models.IntegerField()
    end = models.IntegerField()

    def __str__(self):
        return self.structure.pdb_code.index + " " + protein_segment.slug

    class Meta():
        db_table = "structure_segment"