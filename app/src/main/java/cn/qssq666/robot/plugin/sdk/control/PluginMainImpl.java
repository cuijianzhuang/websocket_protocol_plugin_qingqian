package cn.qssq666.robot.plugin.sdk.control;

import android.os.*;
import android.text.*;
import android.view.*;
import android.view.View.*;
import android.widget.*;
import cn.qssq666.plugindemo.*;
import cn.qssq666.robot.plugin.sdk.interfaces.*;
import java.io.*;
import java.text.*;
import java.util.*;
import org.java_websocket.client.*;
import org.java_websocket.handshake.*;
import org.json.*;
import java.net.*;

public class PluginMainImpl extends SimplePluginInterfaceWrapper
{
    private boolean client_Runing = false;
	
	private StringBuffer tvlog = new StringBuffer();
	
	private WebSocketClient client = null;
	
	
	
	

	@Override
	public int getMinRobotSdk()
	{
		// TODO: Implement this method
		return 0;
	}

	@Override
	public boolean onReceiveRobotFinalCallMsgIsNeedIntercept(IMsgModel p1, List<AtBeanModelI> p2, boolean p3, boolean p4)
	{
		// TODO: Implement this method
		return false;
	}

    private static final String TAG = "PluginMainImpl";

    public File getPicRootdir()
	{
        return new File("/sdcard/qssq666/pic");
    }

    String mLastMsg = "";

    @Override
    public String getAuthorName()
	{
        return "Tick Tock";
    }

    @Override
    public int getVersionCode()
	{
		this.client_Runing = getControlApi().readBooleanConfig("client_Runing",false);
        return 2;
    }

    @Override
    public String getBuildTime()
	{
        return "1999-10-31 00:04:00";
    }

    @Override
    public String getVersionName()
	{
        return "1.1";
    }

    @Override
    public String getPackageName()
	{
        return "cn.qssq666.watchkpic";
    }

    @Override
    public String getDescript()
	{
        return "websocket协议对接其他语言";
    }

    @Override
    public String getPluginName()
	{
        return "Websocket Client";
    }

    @Override
    public boolean isDisable()
	{
        return false;
    }

    @Override
    public void setDisable(boolean disable)
	{

    }

    @Override
    public boolean onReceiveMsgIsNeedIntercept(IMsgModel item)
	{
        mLastMsg = item.getMessage();
        if (getControlApi().isGroupMsg(item))
		{

            if (getConfigApi().isEnableGroupMsg() && getConfigApi().isAtGroupWhiteNames(item))
			{
                return doLogic(item);
            }
        }
		else
		{

            if (getControlApi().isPrivateMsg(item) && getConfigApi().isEnablePrivateReply())
			{

                return doLogic(item);


            }

        }

        return false;
    }

    private boolean doLogic(final IMsgModel item)
	{
		if (this.client_Runing){
		if (client == null){
						try
						{
							client = new WebSocketClient(new URI("ws://" + getControlApi().readStringConfig("server_ip", "0") + ":" + getControlApi().readStringConfig("server_port", "0") + "/")) {

								@Override
								public void onOpen(ServerHandshake arg0)
								{

								}

								@Override
								public void onMessage(String arg0)
								{
									tvlog.append("[websocket] 接收到Json\n");

									try
									{
										JSONObject data = new JSONObject(arg0);
										String action = data.getString("action");
										final String Frienduin = data.getString("Frienduin");
										final String Senderuin = data.getString("Senderuin");
										final String picPath = data.getString("picPath");
										String Message = data.getString("Message");

										if (action.equals("sendMsg"))
										{
											tvlog.append("[robot] 发送消息: " + Message + "\n");
											getControlApi().sendMsg(item.setMessage(Message).setFrienduin(Frienduin));
										}
										else if (action.equals("sendPicMsg"))
										{
											tvlog.append("[robot] 发送图片消息: " + picPath + "\n");
											getControlApi().post(new Runnable() {
													@Override
													public void run()
													{
														getControlApi().sendPicMsg(item, Frienduin, Senderuin, picPath);
													}

												});
										}
										else if (action.equals("sendCardMsg"))
										{
											tvlog.append("[robot] 发送卡片消息\n");
											getControlApi().sendMsgCardMsg(item, Frienduin, Senderuin, picPath);
										}
										else if (action.equals("sendVoiceMsg"))
										{
											tvlog.append("[robot] 发送语音消息: " + picPath + "\n");
											
										    getControlApi().sendVoiceMsg(item.setFrienduin(Frienduin),picPath);
									
										}

									}
									catch (JSONException e)
									{
										tvlog.append(e.toString()+"\n");
									}
								}

								@Override
								public void onError(Exception arg0)
								{
									tvlog.append("[websocket] 发生错误已关闭\n");
									client = null;
								}

								@Override
								public void onClose(int arg0, String arg1, boolean arg2)
								{
									tvlog.append("[websocket] 链接到服务器失败\n");
									client =null;
								}
							};
						}
						catch (URISyntaxException e)
						{
							tvlog.append(e.toString()+"\n");
						}
						
					client.connect();
			}
				
			


        String message = item.getMessage();
		
		mLastMsg = item.getMessage();
		
		 //todo
		String date = new SimpleDateFormat("[yyyy-MM-dd HH:mm:ss]").format(new Date());
		if (item.getIstroop() == 1){
		    tvlog.append("[robot] 群消息 收到来自群: "+item.getFrienduin()+" 的成员: "+item.getNickname()+" 的消息: "+(message)+"\n");
		}else if(item.getIstroop() == 0){
			tvlog.append(date+"[root] 好友消息 收到来自: "+item.getNickname()+" 的消息: "+(message)+"\n");
		}else if(item.getIstroop() == 1000){
			tvlog.append(date+"[robot] 私聊消息 收到来自: "+item.getNickname()+" 的消息: "+(message)+"\n");
		}
		JSONObject data = new JSONObject();
		try
		{
			data.put("Message", message);
			data.put("Frienduin", item.getFrienduin());
			data.put("Senderuin", item.getSenderuin());
			data.put("Istroop", item.getIstroop());
			data.put("Nickname", item.getNickname());
			data.put("Selfuin", item.getSelfuin());
			data.put("Time", item.getTime());
			data.put("Type", item.getType());
		}
		catch (JSONException e)
		{
			tvlog.append(e.toString());
		}
		if (client.isOpen()){
            client.send(data.toString());
		    tvlog.append("[websocket] 消息上传至服务端\n");
		}
		}else{
			tvlog.append("[websocket] 服务未开启\n");
		}
      
		return false;
	}

  

	
	
	
    
    @Override
    public boolean onReceiveOtherIntercept(IMsgModel item, int type)
	{
        return false;
    }


    @Override
    public void onDestory()
	{

    }


    @Override
	public View onConfigUi(ViewGroup viewGroup) {
		this.client_Runing = getControlApi().readBooleanConfig("client_Runing",false);
        LinearLayout linearLayout = new LinearLayout(viewGroup.getContext());
        linearLayout.setOrientation(1);
        linearLayout.setGravity(1);
        final TextView textViewtitle = new TextView(viewGroup.getContext());
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("本插件基于插件sdk版本:2.4开发\n使用方法[ 发送启动websocket 和 停用websocket或websocket状态]\n最后消息:");
        stringBuilder.append(this.mLastMsg);
        textViewtitle.setText(stringBuilder.toString());
        textViewtitle.setPadding(getControlApi().dp2px(5), getControlApi().dp2px(5), getControlApi().dp2px(5), getControlApi().dp2px(5));
        linearLayout.addView(textViewtitle);
        Button buttonEnable = new Button(viewGroup.getContext());
        buttonEnable.setText("启用websocket");
        linearLayout.addView(buttonEnable);
        Button buttondisEnable = new Button(viewGroup.getContext());
        buttondisEnable.setText("停用websocket");
        linearLayout.addView(buttondisEnable);
        TextView textView = new TextView(viewGroup.getContext());
        textView.setTextSize(11.0f);
        textView.setText("远程/内网 websocket服务端ip");
        textView.setPadding(getControlApi().dp2px(5), getControlApi().dp2px(5), getControlApi().dp2px(5), getControlApi().dp2px(5));
        linearLayout.addView(textView);
        EditText editText = new EditText(viewGroup.getContext());
        editText.setHint("请输入websocket服务端ip");
        editText.addTextChangedListener(new Editlistener(this));
        editText.setText(getControlApi().readStringConfig("server_ip","请手动设置"));
        linearLayout.addView(editText);
        textView = new TextView(viewGroup.getContext());
        textView.setText("websocket端口设置");
        textView.setTextSize(11.0f);
        textView.setPadding(getControlApi().dp2px(5), getControlApi().dp2px(5), getControlApi().dp2px(5), getControlApi().dp2px(5));
        linearLayout.addView(textView);
        EditText editText2 = new EditText(viewGroup.getContext());
        editText2.setHint("请输入websocket服务端端口");
        editText2.setText(getControlApi().readStringConfig("server_port","请手动设置"));
        editText2.addTextChangedListener(new Editlistener2(this));
        linearLayout.addView(editText2);
        ScrollView scrollView = new ScrollView(viewGroup.getContext());
        final TextView tvLog = new TextView(viewGroup.getContext());
        scrollView.addView(tvLog);
        linearLayout.addView(scrollView);
        buttondisEnable.setEnabled(this.client_Runing);
        buttonEnable.setEnabled(true ^ this.client_Runing);
        buttonEnable.setOnClickListener(new click_enabled(this,buttonEnable,buttondisEnable));
        buttondisEnable.setOnClickListener(new click_disenabled(this,buttondisEnable,buttonEnable));
		tvLog.setTextSize(8.0f);
		tvLog.setText(tvlog.toString());
	 final Handler mHandler = new Handler() {

		@Override
		public void handleMessage(Message msg)
		{
			super.handleMessage(msg);
			switch (msg.what)
			{
				case 0:
					tvLog.setText(tvlog.toString());
					break;
				default:
					break;
			}
		}

	};
		final Handler mkHandler = new Handler() {

			@Override
			public void handleMessage(Message msg)
			{
				super.handleMessage(msg);
				switch (msg.what)
				{
					case 0:
						StringBuilder stringBuilder = new StringBuilder();
						stringBuilder.append("本插件基于插件sdk版本:2.4开发\n使用方法[ 发送启动websocket 和 停用websocket或websocket状态]\n最后消息:");
						stringBuilder.append(mLastMsg);
						textViewtitle.setText(stringBuilder.toString());

						break;
					default:
						break;
				}
			}

		};
        new Thread(new Runnable(){
				@Override
				public void run()
				{
					int lsat_lenth = tvlog.length();
				   while( true){
					   int length = tvlog.length();
					   if ( lsat_lenth != length){
						   mHandler.sendEmptyMessage(0);
						   mkHandler.sendEmptyMessage(0);
					   }
					   
					   lsat_lenth = length;
					   if (tvlog.length() > 1800 ){
						   tvlog = tvlog.delete(0,1);
					   }
					   
				   }
				}


			}).start();
        return linearLayout;
    }
    
}


class click_enabled implements OnClickListener {
	
	private Button button1;
	private Button button2;
	PluginMainImpl iiii;
    click_enabled(PluginMainImpl iii,Button buttona,Button buttonb) {
		button1 = buttona;
		button2 = buttonb;
		iiii=iii;
    }

    public void onClick(View view) {
        button1.setEnabled(false);
		button2.setEnabled(true);
		iiii.getControlApi().writeConfig("client_Runing",true);
	}
}

class click_disenabled implements OnClickListener {
	private Button button1;
	private Button button2;
	PluginMainImpl iiii;
    click_disenabled(PluginMainImpl iii,Button buttona,Button buttonb) {
		button1 = buttona;
		button2 = buttonb;
		iiii=iii;
    }

    public void onClick(View view) {
        button1.setEnabled(false);
		button2.setEnabled(true);
		iiii.getControlApi().writeConfig("client_Runing",false);
	}
}

class Editlistener implements TextWatcher {
    final /* synthetic */ PluginMainImpl iiii;

    Editlistener(PluginMainImpl iii) {
        this.iiii = iii;
    }

    public void beforeTextChanged(CharSequence s, int start, int count, int after) {
    }

    public void onTextChanged(CharSequence s, int start, int before, int count) {
        this.iiii.getControlApi().writConfig("server_ip",s.toString());
    }

    public void afterTextChanged(Editable s) {
    }
}

class Editlistener implements TextWatcher {
    final /* synthetic */ PluginMainImpl iiii;

    Editlistener(PluginMainImpl iii) {
        this.iiii = iii;
    }

    public void beforeTextChanged(CharSequence s, int start, int count, int after) {
    }

    public void onTextChanged(CharSequence s, int start, int before, int count) {
        this.iiii.getControlApi().writConfig("server_ip",s.toString());
    }

    public void afterTextChanged(Editable s) {
    }
}

class Editlistener2 implements TextWatcher {
    final /* synthetic */ PluginMainImpl iiii;

    Editlistener2(PluginMainImpl iii) {
        this.iiii = iii;
    }

    public void beforeTextChanged(CharSequence s, int start, int count, int after) {
    }

    public void onTextChanged(CharSequence s, int start, int before, int count) {
        this.iiii.getControlApi().writConfig("server_port",s.toString());
    }

    public void afterTextChanged(Editable s) {
    }
}
