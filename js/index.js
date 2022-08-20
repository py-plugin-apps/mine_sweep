import { StreamToStream, createEvent } from "../../../core/client/client.js";
import { segment } from "oicq";

export const rule = {
  mine_sweep_start: {
    reg: "^#扫雷",
    priority: 700,
    describe: "开始扫雷",
  },
  mine_sweep_listener: {
    reg: "noCheck",
    priority: 800,
    describe: "开始扫雷",
  },
  mine_sweep_cancel: {
    reg: "^#取消扫雷",
    priority: 701,
    describe: "取消扫雷",
  },
};

let group_call = {};
let private_call = {};

async function createGame(e) {
  let call = StreamToStream({
    _package: "mine_sweep",
    _handler: "sweep",
    onData: (errors, response) => {
      if (errors) {
        console.log(errors.stack);
      } else {
        let msg = [];

        if (response.message) {
          msg.push(response.message);
        }
        if (response.image.length) {
          msg.push(segment.image(response.image));
        }

        if (response.messageDict.at) {
          msg.push(segment.at(response.messageDict.at));
        }

        e.reply(msg);
      }
    },
    onEnd: () => {
      if (e.isGroup) {
        delete group_call[e.group_id];
      } else {
        delete private_call[e.sender.user_id];
      }
    },
  });

  call.send({
    event: await createEvent(e),
    message: e.msg.replace("#扫雷", ""),
  });

  return {
    participant: {
      owner: e.sender.user_id,
      other: [],
    },
    call: call,
  };
}

function valid(e) {
  if (e.isGroup) {
    let qq = e.sender.user_id;
    let current = group_call[e.group_id].participant;
    return current.allow_all || qq === current.owner || current.other.indexOf(qq) !== -1;
  } else {
    return true;
  }
}

export async function mine_sweep_start(e) {
  if (e.isGroup) {
    if (group_call[e.group_id]) {
      e.reply("扫雷进行中！");
    } else {
      group_call[e.group_id] = await createGame(e);
    }
  } else {
    if (private_call[e.sender.user_id]) {
      e.reply("扫雷进行中！");
    } else {
      private_call[e.sender.user_id] = await createGame(e);
    }
  }
  return true;
}

export async function mine_sweep_listener(e) {
  if (e.isGroup && group_call[e.group_id]) {
    let current = group_call[e.group_id];

    if (e.sender.user_id === group_call[e.group_id].participant.owner && e.msg.startsWith("邀请")) {
      if(e.msg==="邀请所有人"){
        group_call[e.group_id].participant.allow_all=true;
        e.reply(`已允许所有人参与扫雷`);
      }else {
        let at_list = e.message.filter(x => x.type === "at");
        current.participant.other.push(...at_list.map(x => x.qq));
        console.log(current.participant.other);
        e.reply(`已添加${at_list.length}位成员一起扫雷`);
        return true;
      }
    }
    let msg = e.msg.replace("#", "");

    if (msg.startsWith("挖开") || msg.startsWith("标记")) {
      if (valid(e)) {
        current["call"].send({
          message: msg,
        });
        return true;
      } else {
        e.reply(["您还没有被邀请,需要", segment.at(current.participant.owner), "邀请才能参与！"]);
        return true;
      }
    }

  } else if (!e.isGroup && private_call[e.sender.user_id]) {
    let current = private_call[e.sender.user_id];
    let msg = e.msg.replace("#", "");
    if (msg.startsWith("挖开") || msg.startsWith("标记")) {
      current["call"].send({
        message: msg,
      });
      return true;
    }
  }
}

export async function mine_sweep_cancel(e) {
  if (e.isGroup) {
    if (group_call[e.group_id]) {
      if (e.sender.user_id === group_call[e.group_id].participant.owner) {
        group_call[e.group_id]["call"].end();
        e.reply("已取消");
        delete group_call[e.group_id];
      } else {
        e.reply("只有发起人能取消");
      }
    } else {
      e.reply("扫雷未开始");
    }
  } else {
    if (private_call[e.sender.user_id]) {
      private_call[e.sender.user_id]["call"].end();
      delete private_call[e.sender.user_id];
      e.reply("已取消");
    } else {
      e.reply("扫雷未开始");
    }
  }
  return true;
}