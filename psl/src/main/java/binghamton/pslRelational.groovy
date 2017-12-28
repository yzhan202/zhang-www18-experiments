package binghamton;

import java.text.DecimalFormat;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import edu.umd.cs.psl.application.inference.*;
import edu.umd.cs.psl.application.learning.weight.maxlikelihood.MaxLikelihoodMPE;
import edu.umd.cs.psl.application.learning.weight.em.HardEM
import edu.umd.cs.psl.application.learning.weight.em.PairedDualLearner;

import edu.umd.cs.psl.config.*;
import edu.umd.cs.psl.core.*;
import edu.umd.cs.psl.core.inference.*;
import edu.umd.cs.psl.database.*;
import edu.umd.cs.psl.database.rdbms.*;
import edu.umd.cs.psl.database.rdbms.driver.H2DatabaseDriver;
import edu.umd.cs.psl.database.rdbms.driver.H2DatabaseDriver.Type;
import edu.umd.cs.psl.evaluation.result.*;
import edu.umd.cs.psl.evaluation.statistics.*;
import edu.umd.cs.psl.groovy.*;
import edu.umd.cs.psl.groovy.PSLModel;

import edu.umd.cs.psl.model.argument.ArgumentType;
import edu.umd.cs.psl.model.atom.*;
import edu.umd.cs.psl.model.formula.*;
import edu.umd.cs.psl.model.function.*;
import edu.umd.cs.psl.model.kernel.*;
import edu.umd.cs.psl.model.predicate.*;
import edu.umd.cs.psl.model.term.*;
import edu.umd.cs.psl.model.rule.*;
import edu.umd.cs.psl.model.weight.*;
import edu.umd.cs.psl.model.argument.GroundTerm;
import edu.umd.cs.psl.model.parameters.Weight

import edu.umd.cs.psl.ui.loading.*;
import edu.umd.cs.psl.util.database.*;

import com.google.common.collect.Iterables;

import edu.umd.cs.psl.util.database.Queries;

import edu.umd.cs.psl.evaluation.resultui.printer.*;

import java.io.*;
import java.util.*;

import groovy.time.*;

import binghamton.util.FoldUtils
import binghamton.util.GroundingWrapper
import binghamton.util.DataOutputter;

//config manager
ConfigManager cm = ConfigManager.getManager()
ConfigBundle config = cm.getBundle("recovery-model")
Logger log = LoggerFactory.getLogger(this.class)

//database
def defaultPath = System.getProperty("java.io.tmpdir")
String dbpath = config.getString("dbpath", defaultPath + File.separator + "recovery-model")
DataStore data = new RDBMSDataStore(new H2DatabaseDriver(Type.Disk, dbpath, true), config)

PSLModel model = new PSLModel(this, data)

private List<String> getAlcoholWords(){
	def fullFilePath = "data/topAlcoholWords.txt";
	BufferedReader br = new BufferedReader(new FileReader(fullFilePath));
	List<String> topAlcoholWords = new ArrayList<String>();

	try {
		String line = br.readLine();
		while (line != null) {
			topAlcoholWords.add(line)
			line = br.readLine();
		}
	} finally {
		br.close();
	}
	return topAlcoholWords;
}

model.add predicate: "friends", types: [ArgumentType.UniqueID, ArgumentType.UniqueID];
model.add predicate: "localRecovers", types: [ArgumentType.UniqueID];
model.add predicate: "similar", types: [ArgumentType.UniqueID, ArgumentType.UniqueID];
model.add predicate: "usesAlcoholWord", types: [ArgumentType.UniqueID, ArgumentType.String];
model.add predicate: "usesSoberWord", types: [ArgumentType.UniqueID, ArgumentType.String];
model.add predicate: "attendsAA", types: [ArgumentType.UniqueID];

model.add predicate: "recovers", types: [ArgumentType.UniqueID];

model.add predicate: "frequencyAlcoholWord", types: [ArgumentType.UniqueID];
model.add predicate: "frequencySoberWord", types: [ArgumentType.UniqueID];
model.add predicate: "containsAlcoholWord", types: [ArgumentType.UniqueID, ArgumentType.UniqueID, ArgumentType.String];
model.add predicate: "containsSoberWord", types: [ArgumentType.UniqueID, ArgumentType.UniqueID, ArgumentType.String];
model.add predicate: "retweets", types: [ArgumentType.UniqueID, ArgumentType.UniqueID, ArgumentType.UniqueID];
model.add predicate: "replies", types: [ArgumentType.UniqueID, ArgumentType.UniqueID, ArgumentType.UniqueID];

model.add predicate: "topics", types: [ArgumentType.UniqueID, ArgumentType.String];
model.add predicate: "tweetTopics", types: [ArgumentType.UniqueID, ArgumentType.UniqueID, ArgumentType.String];

model.add predicate: "affect", types: [ArgumentType.UniqueID];
model.add predicate: "social", types: [ArgumentType.UniqueID];

model.add predicate: "friendTweetTopic", types: [ArgumentType.UniqueID, ArgumentType.UniqueID, ArgumentType.String];
model.add predicate: "pos_sentiment", types: [ArgumentType.UniqueID, ArgumentType.UniqueID];

model.add predicate: "userTweetTopic", types: [ArgumentType.UniqueID, ArgumentType.UniqueID, ArgumentType.String]


def closedPredicates = [friends, localRecovers, similar, usesAlcoholWord, usesSoberWord, attendsAA, retweets, replies,
	containsAlcoholWord, containsSoberWord, frequencyAlcoholWord, frequencySoberWord, topics, tweetTopics, 
	affect, social, friendTweetTopic, pos_sentiment, userTweetTopic] as Set;

def inferredPredicates = [recovers] as Set;


predicateFileMap = [((Predicate)friends):"friends.txt",
	((Predicate)localRecovers):"localRecovers.txt",
	((Predicate)recovers):"recovers.txt",
	((Predicate)similar):"similarity.txt",
	((Predicate)usesAlcoholWord):"usesAlcoholWord.txt",
	((Predicate)usesSoberWord):"usesSoberWord.txt",
	((Predicate)attendsAA):"attendsAA.txt",

	((Predicate)frequencyAlcoholWord):"frequencyAlcoholWord.txt",
	((Predicate)frequencySoberWord):"frequencySoberWord.txt",
	((Predicate)containsAlcoholWord):"containsAlcoholWord.txt",
	((Predicate)containsSoberWord):"containsSoberWord.txt",
	((Predicate)retweets):"retweets.txt",
	((Predicate)replies):"replies.txt",
	
	((Predicate)topics):"userTopic.txt",
	((Predicate)tweetTopics):"tweetTopic.txt",
	((Predicate)affect):"affect.txt",
	((Predicate)social):"social.txt",
	((Predicate)friendTweetTopic):"friendTweetTopic.txt",
	((Predicate)pos_sentiment):"pos_sentiment.txt",
	
	((Predicate)userTweetTopic):"userTweetTopic.txt"]
	

predicateSoftTruthMap = [((Predicate)friends):false,
	((Predicate)recovers):true,
	((Predicate)localRecovers):true,
	((Predicate)similar):true,
	((Predicate)usesAlcoholWord):false,
	((Predicate)usesSoberWord):false,
	((Predicate)attendsAA):false,
	
	((Predicate)frequencyAlcoholWord):true,
	((Predicate)frequencySoberWord):true,
	((Predicate)containsAlcoholWord):false,
	((Predicate)containsSoberWord):false,
	((Predicate)retweets):false,
	((Predicate)replies):false,
	
	((Predicate)topics):false,
	((Predicate)tweetTopics): false,
	((Predicate)affect):true,
	((Predicate)social):true,
	((Predicate)friendTweetTopic):false,
	((Predicate)pos_sentiment):true,
	
	((Predicate)userTweetTopic):false]


def initialWeight = 5.0

log.info("Defining similarity collective rules..");
model.add( rule : (similar(U1, U2) & recovers(U2)) >> recovers(U1), squared:true, weight : initialWeight)
model.add( rule : (similar(U1, U2) & recovers(U1)) >> recovers(U2), squared:true, weight : initialWeight)
model.add( rule : (similar(U1, U2) & ~recovers(U2)) >> ~recovers(U1), squared:true, weight : initialWeight)
model.add( rule : (similar(U1, U2) & ~recovers(U1)) >> ~recovers(U2), squared:true, weight : initialWeight)

log.info("Defining alcoholic latent variable rules");
Random rand = new Random();
double variance = 0.9
def topAlcoholWords = getAlcoholWords();
for(String aw : topAlcoholWords){

	model.add( rule : (replies(U2, U1, I1) & retweets(U1, U2, I2) & containsAlcoholWord(U1, I2, aw) & attendsAA(U2)) >> ~recovers(U2), squared:true,
		weight :initialWeight)
	model.add( rule : (retweets(U2, U1, I1) & retweets(U1, U2, I2) & containsAlcoholWord(U1, I2, aw) & attendsAA(U2)) >> ~recovers(U2), squared:true,
		weight :initialWeight)
	model.add( rule : (replies(U2, U1, I1) & replies(U1, U2, I2) & containsAlcoholWord(U1, I2, aw) & attendsAA(U2)) >> ~recovers(U2), squared:true,
		weight :initialWeight)
	model.add( rule : (retweets(U2, U1, I1) & replies(U1, U2, I2) & containsAlcoholWord(U1, I2, aw) & attendsAA(U2)) >> ~recovers(U2), squared:true,
		weight :initialWeight)

//    model.add( rule : (friends(U1, U2) & usesAlcoholWord(U2, aw)) >> ~recovers(U1), squared:true,
//		weight : 1)
		
	model.add( rule : (attendsAA(U1) & replies(U1, U2, I) & usesAlcoholWord(U2, aw)) >> ~recovers(U1), squared:true,
		weight : 1)
	model.add( rule : (attendsAA(U1) & retweets(U1, U2, I) & usesAlcoholWord(U2, aw)) >> ~recovers(U1), squared:true,
		weight : 1)
}

for(String sw : ['#recovery', 'sober', 'sobriety', 'recovery', '#sobriety']){
	
	model.add( rule : (replies(U2, U1, I1) & retweets(U1, U2, I2) & containsSoberWord(U1, I2, sw) & attendsAA(U2)) >> recovers(U2), squared:true,
		weight : initialWeight)
	model.add( rule : (replies(U2, U1, I1) & replies(U1, U2, I) & containsSoberWord(U1, I, sw) & attendsAA(U2)) >> recovers(U2), squared:true,
		weight : initialWeight)
	model.add( rule : (retweets(U2, U1, I1) & retweets(U1, U2, I2) & containsSoberWord(U1, I2, sw) & attendsAA(U2)) >> recovers(U2), squared:true,
		weight : initialWeight)
	model.add( rule : (retweets(U2, U1, I1) & replies(U1, U2, I) & containsSoberWord(U1, I, sw) & attendsAA(U2)) >> recovers(U2), squared:true,
		weight : initialWeight)

//	model.add( rule : (friends(U1, U2) & usesSoberWord(U2, sw)) >> recovers(U1), squared:true,
//		weight : 1)
		
	model.add( rule : (attendsAA(U1) & retweets(U1, U2, I) & usesSoberWord(U2, sw)) >> recovers(U1), squared:true,
		weight : 1)
	model.add( rule : (attendsAA(U1) & replies(U1, U2, I) & usesSoberWord(U2, sw)) >> recovers(U1), squared:true,
		weight : 1)

}

Map<CompatibilityKernel,Weight> weights = new HashMap<CompatibilityKernel, Weight>()
for (CompatibilityKernel k : Iterables.filter(model.getKernels(), CompatibilityKernel.class))
	weights.put(k, k.getWeight());

def dataDir = 'data'+java.io.File.separator+'recover_data'+ java.io.File.separator+ 'recover4'
Partition trainPart = new Partition(0)
Partition targetPart = new Partition(1)
def inserter;
for (Predicate p: closedPredicates){
	String fileName = predicateFileMap[p];
	inserter = data.getInserter(p, trainPart);
	def fullFilePath = dataDir + '/' + fileName;
	
	if(predicateSoftTruthMap[p]){
//		println fullFilePath
		InserterUtils.loadDelimitedDataTruth(inserter, fullFilePath, ',');
	}
	else{
		//println fullFilePath
		InserterUtils.loadDelimitedData(inserter, fullFilePath, ',');
	}
}

for (Predicate p: [recovers]){
	String fileName = predicateFileMap[p];
	inserter = data.getInserter(p, targetPart);
	def fullFilePath = dataDir + '/' + fileName;
	if(predicateSoftTruthMap[p]){
		InserterUtils.loadDelimitedDataTruth(inserter, fullFilePath, ',');
	}
	else{
		InserterUtils.loadDelimitedData(inserter, fullFilePath, ',');
	}
}

folds = 5

List<Partition> targetPartitions = new ArrayList<Partition>(folds)
List<Partition> trainWritePartitions = new ArrayList<Partition>(folds)
List<Partition> testWritePartitions = new ArrayList<Partition>(folds)
for (int i=0; i< folds; i++) {
	targetPartitions.add(i, new Partition(i + 2))
	trainWritePartitions.add(i, new Partition(i + 1*folds + 2))
	testWritePartitions.add(i, new Partition(i + 2*folds + 2))
}

List<Set<GroundingWrapper>> groundings = FoldUtils.splitGroundings(data, [recovers], [targetPart], folds)

for (int i = 0; i < folds; i++) {
	FoldUtils.copy(data, targetPart, targetPartitions.get(i), recovers, groundings.get(i))
}

List<List<Double []>> results = new ArrayList<List<Double []>>()
results.add(new ArrayList<Double []>())

for (int fold = 0; fold < folds; fold++){
	/*
	 *  Populate train and test partitions
	 *  TRAIN
	 *  Observed : All
	 *  Target : All except "fold"
	 *  TEST:
	 *  Observed: All
	 *  Target: Only "fold" unobserved, rest observed, predict performance of "fold"
	 */
	
	ArrayList<Partition> trainReadPartitions = new ArrayList<Partition>();
	ArrayList<Partition> testReadPartitions = new ArrayList<Partition>();

	for (int i = 0; i < folds; i++) {
		if (i != fold) {
			trainReadPartitions.add(targetPartitions.get(i))
			testReadPartitions.add(targetPartitions.get(i))
		}
		//
	}
	//testReadPartitions.add(targetPartitions.get(fold))
	testReadPartitions.add(trainPart)
	Partition testLabelPartition = targetPartitions.get(fold)
	
	Database trainDB = data.getDatabase(trainWritePartitions.get(fold), closedPredicates, (Partition []) trainPart)
	
	Database testDB = data.getDatabase(testWritePartitions.get(fold), closedPredicates, (Partition []) testReadPartitions.toArray())

	//Database testDB = data.getDatabase(testWritePartitions.get(fold), closedPredicates, (Partition []) trainPart)
	
	dummy = new Partition(200)
	Partition dummy2 = new Partition(201)
	Partition dummy3 = new Partition(202)
	Database labelsDB = data.getDatabase(dummy, inferredPredicates, (Partition []) trainReadPartitions.toArray())
	
	DataOutputter.outputPredicate("output/training-truth" + fold + ".val" , labelsDB, recovers, ",", true, "User,Truth");
	
	def checkdb = data.getDatabase(targetPart)
	def allGroundings = checkdb.executeQuery(Queries.getQueryForAllAtoms(recovers))
	for (Predicate p : [recovers]) {
		def num = 0
		for (int i = 0; i < allGroundings.size(); i++) {
			GroundTerm [] grounding = allGroundings.get(i)
			GroundAtom atom = testDB.getAtom(p, grounding)
			if (atom instanceof RandomVariableAtom) {
				testDB.commit((RandomVariableAtom) atom);
				
			}
//			else{
//				num ++
//				System.out.println("test_" + num.toString())
//			}
		}
	}
	
	allGroundings = checkdb.executeQuery(Queries.getQueryForAllAtoms(recovers))
	for (Predicate p : [recovers]) {
		def num = 0
		for (int i = 0; i < allGroundings.size(); i++) {
			GroundTerm [] grounding = allGroundings.get(i)
			GroundAtom atom = trainDB.getAtom(p, grounding)
			if (atom instanceof RandomVariableAtom) {
				num++;
				trainDB.commit((RandomVariableAtom) atom);
//				println num
			}
		}
	}
	checkdb.close()

	for (CompatibilityKernel k : Iterables.filter(model.getKernels(), CompatibilityKernel.class)){
		k.setWeight(weights.get(k))
	}
	
	def outputPath = config.getString('experiment.output.outputdir', 'output/'+'crossValidation'+'/');
	File outputDir = new File(outputPath);
	if(!outputDir.exists()) {
		outputDir.mkdirs();
	}
	
	long startTime = System.currentTimeMillis();
	
//	MaxLikelihoodMPE weightLearner = new MaxLikelihoodMPE(model, trainDB, labelsDB, config);
	def weightLearner = new HardEM(model, trainDB, labelsDB, config);
	weightLearner.learn();
	weightLearner.close();
	
	long endTime = System.currentTimeMillis();
	
	long totalTime = endTime - startTime;
	ps = new PrintStream(new FileOutputStream(outputPath + "weightLearningRunningTime", true));
	System.setOut(ps);
	System.out.println(totalTime);
	
	PrintStream ps = new PrintStream(new FileOutputStream(outputPath + "model_"+ fold.toString(), false));
	System.setOut(ps);
	System.out.println("Learned model "+fold.toString() + config.getString("name", "") + "\n" + model.toString())
	
	MPEInference mpe = new MPEInference(model, testDB, config)
	FullInferenceResult result = mpe.mpeInference()
	testDB.close();
	/*
	 * Inferred Values Print
	 */
	Database resultsDB = data.getDatabase(testWritePartitions.get(fold), inferredPredicates )

	ps = new PrintStream(new FileOutputStream(outputPath + "recovers_"+ fold.toString(), false));
	for (GroundAtom atom : Queries.getAllAtoms(resultsDB, recovers)){
		System.setOut(ps);
		System.out.println atom.toString()+ '\t' + atom.getValue()
	}
//	ps = new PrintStream(new FileOutputStream(outputPath + "alcoholic_"+ fold.toString(), false));
//	for (GroundAtom atom : Queries.getAllAtoms(resultsDB, alcoholic)){
//		System.setOut(ps);
//		System.out.println atom.toString()+ '\t' + atom.getValue()
//	}
//	ps = new PrintStream(new FileOutputStream(outputPath + "supportive_"+ fold.toString(), false));
//	for (GroundAtom atom : Queries.getAllAtoms(resultsDB, supportive)){
//		System.setOut(ps);
//		System.out.println atom.toString()+ '\t' + atom.getValue()
//	}
	PrintStream stdout = System.out;
	System.setOut(stdout);
	
	def comparator = new SimpleRankingComparator(resultsDB)
	def groundTruthDB = data.getDatabase(testLabelPartition, inferredPredicates )
	list = Queries.getAllAtoms(groundTruthDB, recovers);
//	println list.size();
	comparator.setBaseline(groundTruthDB)
	
	def metrics = [RankingScore.AUPRC, RankingScore.NegAUPRC, RankingScore.AreaROC, RankingScore.Kendall]
	double [] score = new double[metrics.size()]

	for (int i = 0; i < metrics.size(); i++) {
		comparator.setRankingScore(metrics.get(i))
		score[i] = comparator.compare(recovers)
	}

	ps = new PrintStream(new FileOutputStream(outputPath + "metrics_"+ fold.toString(), false));
	System.setOut(ps);
	System.out.println("Area under positive-class PR curve: " + score[0])
	System.out.println("Area under negative-class PR curve: " + score[1])
	System.out.println("Area under ROC curve: " + score[2])
	System.out.println("Kendall's: " + score[3])

	System.setOut(stdout);
	
	results.get(0).add(fold, score)
	resultsDB.close()
	groundTruthDB.close()
	trainDB.close()
	labelsDB.close()
	
	ps = new PrintStream(new FileOutputStream(outputPath + "logLikelihood", true));
	System.setOut(ps);
	def likelihood = result.getTotalWeightedIncompatibility()
	System.out.println(likelihood.toString())
}

def outputPath = config.getString('experiment.output.outputdir', 'output/'+'crossValidation'+'/');
ps = new PrintStream(new FileOutputStream(outputPath + "final_result", false));
System.setOut(ps);

def methodStats = results.get(0)
def sum = new double[4];
def sumSq = new double[4];
for (int fold = 0; fold < folds; fold++) {
	def score = methodStats.get(fold)
	for (int i = 0; i < 4; i++) {
		sum[i] += score[i];
		sumSq[i] += score[i] * score[i];
	}
	System.out.println("Method " + config + ", fold " + fold +", auprc positive: "
		+ score[0] + ", negative: " + score[1] + ", auROC: " + score[2] + ", kendall: " + score[3])
	
}

//mean = new double[4];
//List<Double> mean = new ArrayList<>(Arrays.asList(0, 0, 0, 0));
//List<Double> variance = new ArrayList<>(Arrays.asList(0, 0, 0, 0));
//variance = new double[4];
for (int i = 0; i < 4; i++) {
	sum[i] = sum[i] / folds;
	sumSq[i] = sumSq[i] / folds - sum[i] * sum[i];
}

System.out.println();
System.out.println("Method " + config + ", auprc positive: (mean/variance) "
		+ sum[0] + "  /  " + sumSq[0] );
System.out.println("Method " + config + ", auprc negative: (mean/variance) "
		+ sum[1] + "  /  " + sumSq[1] );
System.out.println("Method " + config + ", auROC: (mean/variance) "
		+ sum[2] + "  /  " + sumSq[2] );
System.out.println("Method " + config + ", kendall: (mean/variance) "
		+ sum[3] + "  /  " + sumSq[3] );
System.out.println();





