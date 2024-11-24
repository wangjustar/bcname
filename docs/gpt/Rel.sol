// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import "contracts/_Reg.sol";
import "contracts/_Agg.sol";

// 签约合约
contract UserRelation {
    //实例地址
    address instantAddress = address(0);
    // Task struct
    struct Task {
        string title;
        bytes32 seed;
        string desc; // 描述
        uint reward; // 奖励(单块)
        uint nowNum; // 工作者当前数量
        uint unfinishedNum;
        bool finished; // 任务状态
        uint totalNum;
    }
    struct Ware {
        string title;
        string desc;
        bytes32 seed;
        address ppublisherAddr;
        address addr;
        uint status;
        uint blockNum;
        uint copyrightFee;
    }
    struct Refer {
        address referrer;
        bytes32 seed;
    }
    struct Worker {
        address payable workerAddr; // 工作者地址
        uint blocknum;//传输的块数
        uint result; // 评估结果
    }
    //Status for publisher
    enum RS_Status {
        Unknown, // 未知
        Available, // 0 可用
        Waiting, // 1 尽情期待
        Forbidden, // 2 已封禁
        Evaluating // 3 待审核
	}
    // receiver地址
    address receiverAddr;
    // 工作者列表
    Worker[] workerList;
    Refer[] referList;
    // 内含task信息
    Task task;
    // 资源市场信息
    Ware ware;
    // 连接UserReg合约
    UserReg public userReg;
    address public userRegAddress;
    MsgAgg public msgAgg;
    address public msgAggAddress;
    constructor(address _userRegAddress,address _msgAggAddress,bytes32 _seed) {
        // 传递已部署 UserReg 合约的地址作为参数
        userReg = UserReg(_userRegAddress);
        // 保存 UserReg 合约的地址
        userRegAddress = _userRegAddress;
        msgAgg = MsgAgg(_msgAggAddress);
        msgAggAddress = _msgAggAddress;
        task.seed = _seed;
        receiverAddr = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == receiverAddr, "Only owner can call this function");
        _; // 修饰符代码将在此执行
    }

    //初始化种子
    function initialSeed(bytes32 _seed) public onlyOwner{
        if(task.seed == bytes32(0))
        {
            task.seed = _seed;
        }
    }


    //资源匹配
    function WareMatch(bytes32 _seed) public onlyOwner{
        if(_seed!=bytes32(0))
        {
            (string memory title,string memory desc,,address addr,uint status,uint blockNum,uint copyrightFee) = msgAgg.findWareBySeed(_seed);
            ware.title = title;
            ware.desc = desc;
            ware.addr = addr;
            ware.status = status;
            ware.blockNum = blockNum;
            ware.copyrightFee = copyrightFee;
        }
    }

    function addRefer(bytes32 _seed,address _referaddr) public {
        referList.push(Refer(_referaddr,_seed));
    }
    
    
    //发布任务
    function releaseTask(string memory _title,string memory _desc,uint _reward,uint _blockNum,string memory ipaddr) public onlyOwner{
        //匹配ware
        require(task.seed!=bytes32(0),"Seed not designated.");
        ware.seed = task.seed;
        WareMatch(task.seed);
        require(ware.status == 0 || ware.status == 1,"Can't access the resource.");
        //初始化task
        task.title = _title;
        task.desc = _desc;
        task.reward = _reward;
        task.finished = false;
        task.unfinishedNum = 0;
        //匹配失败
        if(task.seed == bytes32(0) || _blockNum == 0)
        {
            task.totalNum = 0;
        }
        //匹配成功
        else{
            task.unfinishedNum = _blockNum;
            task.totalNum = _blockNum;
        }
        msgAgg.deleteDemandmarket(receiverAddr,task.seed);
        msgAgg.findResource(_title, task.seed, _desc,receiverAddr, instantAddress,ipaddr);
    }

    
    // 获取任务信息
    function getTaskInfo() public returns (string memory, bytes32, string memory, address, uint,bool, bool,uint){
        // 更新任务状态
        updateStatus();
        return (task.title, task.seed, task.desc,receiverAddr,task.reward,task.finished,task.totalNum);
    }
    
    // 是否有资质
    function isQualified(address _workerAddr) public view returns (bool) {
        // 判断是否为发布者
        if(receiverAddr == _workerAddr)
            return false;
        return !isWorker(_workerAddr);
    }

    // 判断是否为工作者
    function isWorker(address _workerAddr) public view returns (bool) 
    {
        for(uint i = 0; i < workerList.length; ++i)
            if(workerList[i].workerAddr == _workerAddr)
                return true;
        return false;
    }
    
    // 检查工作者
    function checkWorker() public returns (bool) {
        // 任务时间
        if(task.finished = true)
            return false;
        // 接收者押金
        if(msg.sender.balance < task.reward * task.totalNum)
            return false;
        // 传输可行性
        if(task.seed == bytes32(0) || task.totalNum == 0)
            return false;
        return true;
    }
    
    // 工作者接收任务 payable
    function receiveTask() public payable {
        // 检查条件
        require(isQualified(msg.sender) && checkWorker(),"Not qualified.");
        // 金币不足
        require(msg.value < task.reward,"Not enough value.");
        require(task.seed!= bytes32(0),"Not assigned file.");
        // new Worker
        workerList.push(Worker(payable(msg.sender),0,0));
        // 更新任务状态
        updateStatus();
    }

    // 工作者完成一个块 payable
    function finishTask() public payable {
        uint i = findWorkerId(msg.sender);
        require(i!=65535,"Not workers.");
        workerList[i].blocknum ++;
        task.unfinishedNum --;
        // 更新任务状态
        updateStatus();
    }

    
    // 发布者评估答案
    function evaluateSolution(address _workerAddr, uint _result) public payable {
      // 评估不等于0说明已评估
        uint id = findWorkerId(_workerAddr);
        require(msg.sender == receiverAddr,"Not owner.");
        require(workerList[id].result == 0,"already evaluated.");
        require(task.unfinishedNum == 0  && task.totalNum > 0,"worker still working.");
        workerList[id].result = _result;
        // 发送奖励
        workerList[id].workerAddr.transfer(task.reward*workerList[id].blocknum);
        // 交版权费
        if (ware.addr != address(0)) {
            payable(ware.addr).transfer(ware.copyrightFee);
            }
        // 更新数量
        userReg.dealTask(receiverAddr, 1,task.reward);
        // 更新任务状态
        updateStatus();
    }
    
    // 更新任务状态 内部调用
    function updateStatus() private  {
        if(task.totalNum == 0)
        {
            task.finished = false;
        }
        else if(task.unfinishedNum > 0  && task.totalNum >= task.unfinishedNum)
        task.finished = false;
        else{
            task.finished =true;
            msgAgg.deleteDemandmarket(receiverAddr,task.seed);
            userReg.dealTask(receiverAddr, 0,task.reward*task.totalNum);
        }
    }
    
    // 查找工作者id 内部调用
    function findWorkerId(address _addr) private view returns (uint) {
        for(uint i = 0; i < workerList.length; ++i)
            if(workerList[i].workerAddr== _addr)
                return i;
        return 65535;
    }

    //交易争议
    function reportTrans(address _addr,string memory desc)public {
        msgAgg.addDispute(msg.sender, _addr, instantAddress,desc);
    }
    
}
